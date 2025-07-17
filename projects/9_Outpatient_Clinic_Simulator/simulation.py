"""Outpatient Clinic Simulation Model

Defines clinic resources and patient flow management.
"""

import simpy
import numpy as np
import pandas as pd
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ClinicModel:
    """Outpatient clinic simulation model with configurable resources."""
    
    def __init__(self, env: simpy.Environment, config: Dict[str, Any]):
        """Initialize clinic model with resources."""
        self.env = env
        self.config = config
        
        self._initialize_resources()
        
        self._initialize_data_collection()
        
        self._initialize_counters()
        
        logger.info(f"Clinic initialized with {self.config}")
    
    def _initialize_resources(self):
        """Initialize clinic resources."""
        
        self.doctors = simpy.Resource(
            self.env, 
            capacity=self.config.get('NUM_DOCTORS', 3)
        )
        
        self.nurses = simpy.Resource(
            self.env,
            capacity=self.config.get('NUM_NURSES', 2)
        )
        
        self.registration_staff = simpy.Resource(
            self.env,
            capacity=self.config.get('NUM_REGISTRATION_STAFF', 1)
        )
        
        self.lab_technicians = simpy.Resource(
            self.env,
            capacity=self.config.get('NUM_LAB_TECHNICIANS', 1)
        )
        
        self.exam_rooms = simpy.Resource(
            self.env,
            capacity=self.config.get('NUM_EXAM_ROOMS', 4)
        )
        
        self.waiting_room_capacity = simpy.Container(
            self.env,
            capacity=self.config.get('WAITING_ROOM_CAPACITY', 50),
            init=self.config.get('WAITING_ROOM_CAPACITY', 50)
        )
        
        self.lab_equipment = simpy.Resource(
            self.env,
            capacity=self.config.get('NUM_LAB_EQUIPMENT', 2)
        )
        
        self.pharmacy_counter = simpy.Resource(
            self.env,
            capacity=self.config.get('NUM_PHARMACY_COUNTERS', 1)
        )
        
        logger.info("Resources initialized:")
        logger.info(f"  - Doctors: {self.doctors.capacity}")
        logger.info(f"  - Nurses: {self.nurses.capacity}")
        logger.info(f"  - Exam Rooms: {self.exam_rooms.capacity}")
        logger.info(f"  - Registration Staff: {self.registration_staff.capacity}")
        logger.info(f"  - Lab Technicians: {self.lab_technicians.capacity}")
        logger.info(f"  - Lab Equipment: {self.lab_equipment.capacity}")
        logger.info(f"  - Pharmacy Counters: {self.pharmacy_counter.capacity}")
        logger.info(f"  - Waiting Room Capacity: {self.waiting_room_capacity.capacity}")
    
    def _initialize_data_collection(self):
        """Initialize data collection."""
        self.patient_log = []
        self.resource_utilization_log = []
        self.event_log = []
        
        self.resource_utilization = {
            'doctors': [],
            'nurses': [],
            'registration_staff': [],
            'lab_technicians': [],
            'exam_rooms': [],
            'lab_equipment': [],
            'pharmacy_counter': []
        }
    
    def _initialize_counters(self):
        """Initialize counters."""
        self.patient_counter = 0
        self.patients_served = 0
        self.patients_balked = 0
        self.patients_in_system = 0
    
    def get_resource_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current status of all resources."""
        status = {}
        
        resources = {
            'doctors': self.doctors,
            'nurses': self.nurses,
            'registration_staff': self.registration_staff,
            'lab_technicians': self.lab_technicians,
            'exam_rooms': self.exam_rooms,
            'lab_equipment': self.lab_equipment,
            'pharmacy_counter': self.pharmacy_counter
        }
        
        for name, resource in resources.items():
            status[name] = {
                'capacity': resource.capacity,
                'in_use': len(resource.users),
                'queue_length': len(resource.queue),
                'utilization': len(resource.users) / resource.capacity if resource.capacity > 0 else 0
            }
        
        # Waiting room handling
        status['waiting_room'] = {
            'capacity': self.waiting_room_capacity.capacity,
            'available': self.waiting_room_capacity.level,
            'occupied': self.waiting_room_capacity.capacity - self.waiting_room_capacity.level,
            'utilization': (self.waiting_room_capacity.capacity - self.waiting_room_capacity.level) / self.waiting_room_capacity.capacity
        }
        
        return status
    
    def log_event(self, event_type: str, patient_id: str, details: Dict[str, Any]):
        """Log simulation events."""
        event = {
            'timestamp': self.env.now,
            'event_type': event_type,
            'patient_id': patient_id,
            'details': details
        }
        self.event_log.append(event)
    
    def log_resource_utilization(self):
        """Log resource utilization."""
        status = self.get_resource_status()
        
        utilization_record = {
            'timestamp': self.env.now,
            'resource_status': status
        }
        
        self.resource_utilization_log.append(utilization_record)
        
        # Update tracking
        for resource_name, resource_data in status.items():
            if resource_name in self.resource_utilization:
                self.resource_utilization[resource_name].append({
                    'time': self.env.now,
                    'utilization': resource_data['utilization']
                })
    
    def check_system_capacity(self) -> bool:
        """Check if system has capacity for new patients."""
        # Check waiting room
        if self.waiting_room_capacity.level <= 0:
            return False
        
        # Check system limit
        max_patients = self.config.get('MAX_PATIENTS_IN_SYSTEM', 100)
        if self.patients_in_system >= max_patients:
            return False
        
        return True
    
    def get_simulation_statistics(self) -> Dict[str, Any]:
        """Get simulation statistics."""
        stats = {
            'patients_served': self.patients_served,
            'patients_balked': self.patients_balked,
            'patients_in_system': self.patients_in_system,
            'total_patients': self.patient_counter,
            'current_time': self.env.now
        }
        
        # Add utilization stats
        resource_stats = {}
        for resource_name, utilization_data in self.resource_utilization.items():
            if utilization_data:
                resource_stats[f'{resource_name}_avg_utilization'] = np.mean([u['utilization'] for u in utilization_data])
                resource_stats[f'{resource_name}_max_utilization'] = np.max([u['utilization'] for u in utilization_data])
        
        stats.update(resource_stats)
        
        return stats

def create_clinic_simulation(config: Dict[str, Any]) -> tuple[simpy.Environment, ClinicModel]:
    """Create a clinic simulation environment."""
    env = simpy.Environment()
    
    clinic = ClinicModel(env, config)
    
    logger.info("Clinic simulation environment created successfully")
    
    return env, clinic

DEFAULT_CLINIC_CONFIG = {
    'NUM_DOCTORS': 3,
    'NUM_NURSES': 2,
    'NUM_REGISTRATION_STAFF': 1,
    'NUM_LAB_TECHNICIANS': 1,
    
    'NUM_EXAM_ROOMS': 5,
    'NUM_LAB_EQUIPMENT': 2,
    'NUM_PHARMACY_COUNTERS': 1,
    'WAITING_ROOM_CAPACITY': 50,
    
    'MAX_PATIENTS_IN_SYSTEM': 100,
    
    'SIMULATION_TIME': 120,  # 2 hours in minutes
    'RANDOM_SEED': 42
}

def main():
    """Demonstrate clinic model setup."""
    print("=" * 60)
    print("OUTPATIENT CLINIC SIMULATION - STEP 1.2")
    print("Clinic Model and Resources Definition")
    print("=" * 60)
    
    env, clinic = create_clinic_simulation(DEFAULT_CLINIC_CONFIG)
    
    print("\nInitial Resource Status:")
    print("-" * 40)
    
    status = clinic.get_resource_status()
    for resource_name, resource_data in status.items():
        print(f"{resource_name.replace('_', ' ').title()}:")
        if 'in_use' in resource_data:
            print(f"  Capacity: {resource_data['capacity']}")
            print(f"  Available: {resource_data['capacity'] - resource_data['in_use']}")
            print(f"  Queue Length: {resource_data['queue_length']}")
            print(f"  Utilization: {resource_data['utilization']:.1%}")
        else:
            # Waiting room
            print(f"  Capacity: {resource_data['capacity']}")
            print(f"  Available: {resource_data['available']}")
            print(f"  Occupied: {resource_data['occupied']}")
            print(f"  Utilization: {resource_data['utilization']:.1%}")
        print()
    
    print("Simulation Statistics:")
    print("-" * 40)
    stats = clinic.get_simulation_statistics()
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n✅ Clinic model and resources successfully defined!")
    print("Ready for patient flow implementation in next steps.")

if __name__ == "__main__":
    main()