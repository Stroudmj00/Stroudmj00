"""Realistic Patient Journey - Outpatient Clinic Simulation

Implements realistic patient flow:
1. Patient arrives and waits
2. Registration nurse checks in patient
3. Patient moves to exam room
4. Nurse assessment
5. Doctor consultation
6. Patient discharge
"""

import simpy
import numpy as np
import pandas as pd
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealisticPatientJourney:
    """Manages patient journey data and statistics."""
    
    def __init__(self):
        self.journey_data = []
        self.current_patients = {}
        self.waiting_room_patients = set()
        self.exam_room_patients = {}
        self.patient_states = {}
    
    def start_journey(self, patient_id: str, arrival_time: float):
        """Start patient journey."""
        self.current_patients[patient_id] = {
            'patient_id': patient_id,
            'arrival_time': arrival_time,
            'waiting_room_start': arrival_time,
            'registration_start': None,
            'registration_end': None,
            'exam_room_assigned': None,
            'nurse_visit_start': None,
            'nurse_visit_end': None,
            'doctor_visit_start': None,
            'doctor_visit_end': None,
            'departure_time': None,
            'room_id': None
        }
        self.waiting_room_patients.add(patient_id)
        self.patient_states[patient_id] = 'waiting_room'
    
    def log_event(self, patient_id: str, event: str, time: float, **kwargs):
        """Log patient journey event."""
        if patient_id in self.current_patients:
            self.current_patients[patient_id][event] = time
            for key, value in kwargs.items():
                self.current_patients[patient_id][key] = value
    
    def move_to_exam_room(self, patient_id: str, room_id: int, time: float):
        """Move patient to exam room."""
        if patient_id in self.waiting_room_patients:
            self.waiting_room_patients.remove(patient_id)
            self.exam_room_patients[room_id] = patient_id
            self.patient_states[patient_id] = 'exam_room'
            self.current_patients[patient_id]['room_id'] = room_id
            self.current_patients[patient_id]['exam_room_assigned'] = time
    
    def discharge_patient(self, patient_id: str, time: float):
        """Discharge patient."""
        if patient_id in self.current_patients:
            room_id = self.current_patients[patient_id]['room_id']
            if room_id is not None and room_id in self.exam_room_patients:
                del self.exam_room_patients[room_id]
            
            self.current_patients[patient_id]['departure_time'] = time
            self.patient_states[patient_id] = 'discharged'
            
            # Calculate metrics
            journey = self.current_patients[patient_id]
            total_time = time - journey['arrival_time']
            waiting_time = (journey['exam_room_assigned'] - journey['arrival_time']) if journey['exam_room_assigned'] else 0
            
            self.journey_data.append({
                **journey,
                'total_time': total_time,
                'waiting_time': waiting_time,
                'service_completed': True
            })
    
    def get_waiting_room_count(self):
        """Get waiting room patient count."""
        return len(self.waiting_room_patients)
    
    def get_exam_room_occupancy(self):
        """Get exam room occupancy."""
        return self.exam_room_patients.copy()

def realistic_patient_process(env: simpy.Environment, patient_id: str, clinic, journey_tracker: RealisticPatientJourney, 
                            service_time_config: Dict[str, Dict[str, float]]):
    """Patient journey generator function.
    
    Flow: Arrival -> Registration -> Exam Room -> Nurse -> Doctor -> Discharge
    """
    
    # STEP 1: ARRIVAL
    arrival_time = env.now
    journey_tracker.start_journey(patient_id, arrival_time)
    
    logger.info(f"Patient {patient_id} arrives and sits in waiting room at time {arrival_time:.2f}")
    clinic.log_event('arrival', patient_id, {'time': arrival_time})
    
    # STEP 2: REGISTRATION
    with clinic.registration_staff.request() as reg_req:
        yield reg_req
        
        registration_start = env.now
        journey_tracker.log_event(patient_id, 'registration_start', registration_start)
        
        logger.info(f"Registration nurse visits Patient {patient_id} in waiting room at time {registration_start:.2f}")
        
        # Service time
        reg_config = service_time_config.get('registration', {'mean': 3.0, 'std': 0.8})
        reg_time = max(0.5, np.random.normal(loc=reg_config['mean'], scale=reg_config['std']))
        
        yield env.timeout(reg_time)
        
        registration_end = env.now
        journey_tracker.log_event(patient_id, 'registration_end', registration_end)
        
        logger.info(f"Registration complete for Patient {patient_id} at time {registration_end:.2f} (took {reg_time:.2f} min)")
        clinic.log_event('registration_complete', patient_id, {'time': registration_end, 'duration': reg_time})
    
    # STEP 3: WAIT FOR EXAM ROOM
    logger.info(f"Patient {patient_id} waits for exam room at time {env.now:.2f}")
    
    with clinic.exam_rooms.request() as room_req:
        yield room_req
        
        exam_room_time = env.now
        # Assign room
        # Get room count
        num_rooms = clinic.config.get('NUM_EXAM_ROOMS', 5)
        available_rooms = [i for i in range(num_rooms) if i not in journey_tracker.exam_room_patients]
        room_id = available_rooms[0] if available_rooms else 0
        
        journey_tracker.move_to_exam_room(patient_id, room_id, exam_room_time)
        
        logger.info(f"Patient {patient_id} moves to exam room {room_id} at time {exam_room_time:.2f}")
        clinic.log_event('exam_room_assigned', patient_id, {'time': exam_room_time, 'room_id': room_id})
        
        # STEP 4: NURSE VISIT
        with clinic.nurses.request() as nurse_req:
            yield nurse_req
            
            nurse_start = env.now
            journey_tracker.log_event(patient_id, 'nurse_visit_start', nurse_start)
            
            logger.info(f"Nurse visits Patient {patient_id} in room {room_id} at time {nurse_start:.2f}")
            
            # Service time
            nurse_config = service_time_config.get('nurse_visit', {'mean': 8.0, 'std': 2.0})
            nurse_time = max(1.0, np.random.normal(loc=nurse_config['mean'], scale=nurse_config['std']))
            
            yield env.timeout(nurse_time)
            
            nurse_end = env.now
            journey_tracker.log_event(patient_id, 'nurse_visit_end', nurse_end)
            
            logger.info(f"Nurse completes visit with Patient {patient_id} at time {nurse_end:.2f} (took {nurse_time:.2f} min)")
            clinic.log_event('nurse_visit_complete', patient_id, {'time': nurse_end, 'duration': nurse_time})
        
        # STEP 5: DOCTOR VISIT
        with clinic.doctors.request() as doc_req:
            yield doc_req
            
            doctor_start = env.now
            journey_tracker.log_event(patient_id, 'doctor_visit_start', doctor_start)
            
            logger.info(f"Doctor visits Patient {patient_id} in room {room_id} at time {doctor_start:.2f}")
            
            # Service time
            doctor_config = service_time_config.get('doctor_visit', {'mean': 12.0, 'std': 4.0})
            doctor_time = max(2.0, np.random.normal(loc=doctor_config['mean'], scale=doctor_config['std']))
            
            yield env.timeout(doctor_time)
            
            doctor_end = env.now
            journey_tracker.log_event(patient_id, 'doctor_visit_end', doctor_end)
            
            logger.info(f"Doctor completes visit with Patient {patient_id} at time {doctor_end:.2f} (took {doctor_time:.2f} min)")
            clinic.log_event('doctor_visit_complete', patient_id, {'time': doctor_end, 'duration': doctor_time})
        
        # STEP 6: DISCHARGE
        departure_time = env.now
        journey_tracker.discharge_patient(patient_id, departure_time)
        
        logger.info(f"Patient {patient_id} discharged at time {departure_time:.2f}")
        clinic.log_event('discharge', patient_id, {'time': departure_time})

def run_realistic_simulation(clinic_config: Dict[str, Any] = None,
                           service_time_config: Dict[str, Dict[str, float]] = None,
                           simulation_duration: float = 120,
                           arrival_rate: float = 5.0,
                           random_seed: int = 42) -> Dict[str, Any]:
    """Run realistic clinic simulation with proper patient flow."""
    
    np.random.seed(random_seed)
    
    # Default configurations
    if clinic_config is None:
        from simulation import DEFAULT_CLINIC_CONFIG
        clinic_config = DEFAULT_CLINIC_CONFIG
    
    if service_time_config is None:
        service_time_config = {
            'registration': {'mean': 3.0, 'std': 0.8},
            'nurse_visit': {'mean': 8.0, 'std': 2.0},
            'doctor_visit': {'mean': 12.0, 'std': 4.0}
        }
    
    env = simpy.Environment()
    
    from simulation import create_clinic_simulation
    env, clinic = create_clinic_simulation(clinic_config)
    journey_tracker = RealisticPatientJourney()
    
    def patient_arrivals():
        patient_count = 0
        while True:
            # Inter-arrival time
            inter_arrival = np.random.exponential(arrival_rate)
            yield env.timeout(inter_arrival)
            
            patient_count += 1
            patient_id = f"Patient_{patient_count:03d}"
            
            # Start process
            env.process(realistic_patient_process(env, patient_id, clinic, journey_tracker, service_time_config))
    
    env.process(patient_arrivals())
    
    env.run(until=simulation_duration)
    
    return {
        'journey_data': journey_tracker.journey_data,
        'patient_journey_summary': pd.DataFrame(journey_tracker.journey_data),
        'simulation_duration': simulation_duration,
        'total_patients': len(journey_tracker.journey_data),
        'clinic_config': clinic_config,
        'service_time_config': service_time_config
    }

if __name__ == "__main__":
    results = run_realistic_simulation(simulation_duration=60)
    
    print("=" * 60)
    print("REALISTIC OUTPATIENT CLINIC SIMULATION")
    print("=" * 60)
    
    df = results['patient_journey_summary']
    if not df.empty:
        print(f"Total patients processed: {len(df)}")
        print(f"Average total time: {df['total_time'].mean():.2f} minutes")
        print(f"Average waiting time: {df['waiting_time'].mean():.2f} minutes")
        print(f"Max waiting time: {df['waiting_time'].max():.2f} minutes")
    else:
        print("No patients completed their journey in the simulation time.")