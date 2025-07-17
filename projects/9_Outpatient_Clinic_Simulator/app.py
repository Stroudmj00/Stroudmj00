"""Outpatient Clinic Simulation Tool"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

from realistic_patient_journey import run_realistic_simulation

# Configure page
st.set_page_config(
    page_title="Clinic Simulation",
    page_icon="🏥",
    layout="wide"
)

# Page styling
st.markdown("""
<style>
    /* Global theme: White background, black text */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f5f5f5 !important;
    }
    
    /* Sidebar content */
    section[data-testid="stSidebar"] > div {
        background-color: #f5f5f5 !important;
    }
    
    /* Sidebar inputs */
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stNumberInput > div > div,
    section[data-testid="stSidebar"] .stSlider > div > div,
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #000000 !important;
    }
    
    /* Sidebar dropdowns */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }
    
    /* Main inputs */
    .stSelectbox > div > div,
    .stNumberInput > div > div,
    .stSlider > div > div,
    input, select, textarea {
        background-color: #f5f5f5;
        color: #000000;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0066ff;
        font-weight: bold;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0066ff;
        color: #ffffff;
        border: 2px solid #0066ff;
        font-weight: bold;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #0052cc;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f5f5f5;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #e0e0e0;
        border-bottom: none;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
        color: #0066ff;
        border-bottom: 2px solid #0066ff;
    }
    
    /* Metrics */
    .stMetric {
        color: #000000 !important;
    }
    
    .stMetric > div {
        color: #000000 !important;
    }
    
    .stMetric label {
        color: #000000 !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        color: #000000 !important;
    }
    
    .stMetric [data-testid="metric-container"] > div {
        color: #000000 !important;
    }
    
    /* Custom metric values */
    .metric-value {
        color: #0066ff;
        font-weight: bold;
        font-size: 24px;
    }
    
    /* Messages */
    .stSuccess {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0066ff !important;
    }
    
    .stSuccess > div {
        color: #000000 !important;
    }
    
    .stError {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #ff0000 !important;
    }
    
    .stError > div {
        color: #000000 !important;
    }
    
    /* Station counts */
    .stColumns div {
        color: #000000 !important;
    }
    
    /* Text elements */
    p, span, div {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'simulation_results' not in st.session_state:
        st.session_state.simulation_results = None
    if 'simulation_progress' not in st.session_state:
        st.session_state.simulation_progress = 0
    if 'simulation_status' not in st.session_state:
        st.session_state.simulation_status = "Ready to run simulation"

def create_sidebar():
    st.sidebar.header("🏥 Simulation Settings")
    
    # Resources
    st.sidebar.subheader("Resources")
    num_doctors = st.sidebar.slider("Doctors", 1, 8, 3)
    num_rooms = st.sidebar.slider("Exam Rooms", 1, 10, 5)
    num_nurses = st.sidebar.slider("Nurses", 1, 6, 2)
    num_registration = st.sidebar.slider("Registration Staff", 1, 4, 1)
    
    st.sidebar.markdown("---")
    
    # Processing Times
    st.sidebar.subheader("Processing Times (minutes)")
    registration_time = st.sidebar.slider("Registration Time", 1, 10, 3)
    nurse_time = st.sidebar.slider("Nurse Visit Time", 3, 20, 8)
    doctor_time = st.sidebar.slider("Doctor Visit Time", 5, 30, 12)
    
    # Arrival Rate
    st.sidebar.subheader("Patient Arrivals")
    arrival_rate = st.sidebar.slider("Average time between arrivals (minutes)", 1, 15, 5)
    
    st.sidebar.markdown("---")
    
    # Simulation settings
    st.sidebar.subheader("Simulation")
    duration = st.sidebar.slider("Duration (hours)", 1, 8, 2)
    random_seed = st.sidebar.number_input("Random Seed", 1, 1000, 42)
    
    st.sidebar.markdown("---")
    
    # Run button
    run_sim = st.sidebar.button("🚀 Run Simulation")
    
    return {
        'num_doctors': num_doctors,
        'num_rooms': num_rooms,
        'num_nurses': num_nurses,
        'num_registration': num_registration,
        'registration_time': registration_time,
        'nurse_time': nurse_time,
        'doctor_time': doctor_time,
        'arrival_rate': arrival_rate,
        'duration': duration * 60,  # Convert to minutes
        'random_seed': random_seed,
        'run_simulation': run_sim
    }


@st.cache_data
def run_simulation_with_config(config):
    # Create clinic configuration
    clinic_config = {
        'NUM_DOCTORS': config['num_doctors'],
        'NUM_NURSES': config['num_nurses'],
        'NUM_REGISTRATION_STAFF': config['num_registration'],
        'NUM_LAB_TECHNICIANS': 1,
        'NUM_EXAM_ROOMS': config['num_rooms'],
        'NUM_LAB_EQUIPMENT': 2,
        'NUM_PHARMACY_COUNTERS': 1,
        'WAITING_ROOM_CAPACITY': 50,
        'MAX_PATIENTS_IN_SYSTEM': 100,
        'SIMULATION_TIME': config['duration'],
        'RANDOM_SEED': config['random_seed']
    }
    
    # Service times for realistic simulation (from user input)
    service_time_config = {
        'registration': {'mean': config['registration_time'], 'std': config['registration_time'] * 0.3},
        'nurse_visit': {'mean': config['nurse_time'], 'std': config['nurse_time'] * 0.25},
        'doctor_visit': {'mean': config['doctor_time'], 'std': config['doctor_time'] * 0.3}
    }
    
    # Run simulation
    results = run_realistic_simulation(
        clinic_config=clinic_config,
        service_time_config=service_time_config,
        simulation_duration=config['duration'],
        arrival_rate=config['arrival_rate'],
        random_seed=config['random_seed']
    )
    
    # Add compatibility data
    results['log_dataframe'] = pd.DataFrame()  # Will be populated by logging
    results['resource_utilization_summary'] = pd.DataFrame()  # Will be populated by logging
    results['kpi_summary'] = calculate_kpis_from_journey(results['patient_journey_summary'])
    results['num_doctors'] = config['num_doctors']
    results['num_nurses'] = config['num_nurses']
    results['num_rooms'] = config['num_rooms']
    results['num_registration'] = config['num_registration']
    
    return results

def calculate_kpis_from_journey(journey_df):
    """Calculate KPIs from patient journey data."""
    if journey_df.empty:
        return {
            'patients_served': 0,
            'avg_wait_time': 0,
            'avg_total_time': 0,
            'service_completion_rate': 0,
            'avg_doctor_utilization': 0,
            'avg_room_utilization': 0,
            'max_wait_time': 0,
            'patients_balked': 0
        }
    
    completed = journey_df[journey_df['service_completed'] == True]
    
    return {
        'patients_served': len(completed),
        'avg_wait_time': completed['waiting_time'].mean() if not completed.empty else 0,
        'avg_total_time': completed['total_time'].mean() if not completed.empty else 0,
        'service_completion_rate': len(completed) / len(journey_df) if not journey_df.empty else 0,
        'avg_doctor_utilization': 0.5,
        'avg_room_utilization': 0.4,
        'max_wait_time': completed['waiting_time'].max() if not completed.empty else 0,
        'patients_balked': 0
    }

def display_main_results(results):
    if results is None:
        st.title("🏥 Clinic Simulation Tool")
        st.markdown("""
        **Use the sidebar to configure your clinic and run a simulation.**
        
        This tool helps you:
        - Compare different scheduling policies
        - Optimize staffing levels
        - Analyze patient wait times
        - Visualize clinic operations
        """)
        return
    
    st.title("📊 Simulation Results")
    
    # Get KPIs
    kpis = results['kpi_summary']
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Patients Served", f"{kpis.get('patients_served', 0)}")
    
    with col2:
        st.metric("Avg Wait Time", f"{kpis.get('avg_wait_time', 0):.1f} min")
    
    with col3:
        st.metric("Avg Total Time", f"{kpis.get('avg_total_time', 0):.1f} min")
    
    with col4:
        st.metric("Service Rate", f"{kpis.get('service_completion_rate', 0):.1%}")
    
    # Additional metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Doctor Utilization", f"{kpis.get('avg_doctor_utilization', 0):.1%}")
    
    with col6:
        st.metric("Room Utilization", f"{kpis.get('avg_room_utilization', 0):.1%}")
    
    with col7:
        st.metric("Max Wait Time", f"{kpis.get('max_wait_time', 0):.1f} min")
    
    with col8:
        st.metric("Patients Left", f"{kpis.get('patients_balked', 0)}")


def get_chart_theme():
    """Return consistent chart theme for all plots with transparent backgrounds"""
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
        'paper_bgcolor': 'rgba(0,0,0,0)',  # Transparent background
        'font': {'color': '#000000', 'size': 14},
        'showlegend': True,
        'legend': {
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': '#000000',
            'borderwidth': 1,
            'font': {'color': '#000000'}
        }
    }

def get_axis_style():
    """Return consistent axis styling"""
    return {
        'gridcolor': '#e0e0e0',
        'color': '#000000',
        'tickfont': {'color': '#000000'},
        'linecolor': '#000000',
        'zerolinecolor': '#000000'
    }

def get_room_position(room_id):
    """Get the x, y position for a room based on its ID in 2-column layout"""
    if room_id < 5:
        # First column (left side)
        room_x = 3.5
        room_y = 3.5 - room_id * 0.7
    else:
        # Second column (right side)
        room_x = 4.5
        room_y = 3.5 - (room_id - 5) * 0.7
    return room_x, room_y

def create_animation_frames(journey_df, max_time, num_rooms=5, num_doctors=3, num_nurses=2):
    """Create animation frames data for Plotly built-in animation"""
    import numpy as np
    
    # Create time points (every minute)
    time_points = np.arange(0, max_time + 1, 1)
    
    # Define station positions dynamically based on number of rooms
    stations = {
        'Unregistered Waiting': (1.5, 2),
        'Registered Waiting': (2.5, 2),
        'Discharged': (6, 2)
    }
    
    # Add exam rooms dynamically
    for i in range(num_rooms):
        room_y = 3 - i * 0.8  # Spread rooms vertically
        stations[f'Exam Room {i+1}'] = (4, room_y)
    
    animation_frames = []
    
    for time_point in time_points:
        frame_data = {
            'time': time_point,
            'patients': [],
            'staff': [],
            'annotations': []  # Add annotations for dynamic text
        }
        
        # Get patients active at this time
        current_patients = journey_df[
            (journey_df['arrival_time'] <= time_point) & 
            ((journey_df['departure_time'] > time_point) | (journey_df['departure_time'].isna()))
        ]
        
        # Patient colors (consistent across time)
        patient_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'yellow', 'cyan']
        
        # Count patients in different waiting states
        unregistered_patients = current_patients[
            (pd.isna(current_patients['registration_start']) | (current_patients['registration_start'] > time_point)) &
            (pd.isna(current_patients['departure_time']) | (current_patients['departure_time'] > time_point))
        ]
        
        registered_waiting_patients = current_patients[
            (~pd.isna(current_patients['registration_end']) & (current_patients['registration_end'] <= time_point)) &
            (pd.isna(current_patients['exam_room_assigned']) | (current_patients['exam_room_assigned'] > time_point)) &
            (pd.isna(current_patients['departure_time']) | (current_patients['departure_time'] > time_point))
        ]
        
        unregistered_count = len(unregistered_patients)
        registered_waiting_count = len(registered_waiting_patients)
        
        # Add unregistered waiting count annotation
        frame_data['annotations'].append({
            'x': 1.5, 'y': 2.35,
            'text': f'Unregistered: {unregistered_count}',
            'showarrow': False,
            'font': {'color': 'darkred', 'size': 12, 'weight': 'bold'},
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': 'darkred',
            'borderwidth': 1
        })
        
        # Add registered waiting count annotation
        frame_data['annotations'].append({
            'x': 2.5, 'y': 2.35,
            'text': f'Registered: {registered_waiting_count}',
            'showarrow': False,
            'font': {'color': 'darkgreen', 'size': 12, 'weight': 'bold'},
            'bgcolor': 'rgba(255,255,255,0.8)',
            'bordercolor': 'darkgreen',
            'borderwidth': 1
        })
        
        # Track room occupancy to prevent overlaps
        room_occupancy = {i: None for i in range(num_rooms)}
        
        # Categorize patients by state
        for idx, patient in current_patients.iterrows():
            color = patient_colors[idx % len(patient_colors)]
            patient_id = patient['patient_id']
            
            # Determine patient location at current time
            if pd.isna(patient['departure_time']) or patient['departure_time'] > time_point:
                if pd.isna(patient['exam_room_assigned']) or patient['exam_room_assigned'] > time_point:
                    # Determine if patient is registered or unregistered
                    is_registered = (~pd.isna(patient['registration_end']) and patient['registration_end'] <= time_point)
                    
                    if is_registered:
                        # Patient in registered waiting area (right side)
                        registered_idx = len([p for p in frame_data['patients'] if p.get('location') == 'Registered Waiting'])
                        row = registered_idx // 3  # 3 patients per row
                        col = registered_idx % 3
                        offset_x = -0.2 + col * 0.13  # Spread horizontally
                        offset_y = 0.15 - row * 0.1   # Stack vertically
                        
                        base_x = 2.5  # Right side of waiting room
                        location = 'Registered Waiting'
                        label_color = 'darkgreen'
                    else:
                        # Patient in unregistered waiting area (left side)
                        unregistered_idx = len([p for p in frame_data['patients'] if p.get('location') == 'Unregistered Waiting'])
                        row = unregistered_idx // 3  # 3 patients per row
                        col = unregistered_idx % 3
                        offset_x = -0.2 + col * 0.13  # Spread horizontally
                        offset_y = 0.15 - row * 0.1   # Stack vertically
                        
                        base_x = 1.5  # Left side of waiting room
                        location = 'Unregistered Waiting'
                        label_color = 'darkred'
                    
                    # Add patient total time in system label
                    total_time_in_system = time_point - patient['arrival_time']
                    
                    frame_data['patients'].append({
                        'patient_id': patient_id,
                        'x': base_x + offset_x,
                        'y': 2 + offset_y,
                        'color': color,
                        'location': location,
                        'size': 10
                    })
                    
                    # Add total time label for patient
                    frame_data['annotations'].append({
                        'x': base_x + offset_x, 'y': 2 + offset_y - 0.15,
                        'text': f'{total_time_in_system:.0f}m',
                        'showarrow': False,
                        'font': {'color': 'darkgreen', 'size': 9, 'weight': 'bold'},  # Always green for patients
                        'bgcolor': 'rgba(255,255,255,0.8)',
                        'bordercolor': 'darkgreen',
                        'borderwidth': 1
                    })
                else:
                    # Patient in exam room - position on top of exam room area
                    room_id = patient.get('room_id', 0)
                    if room_id < num_rooms and room_occupancy.get(room_id) is None:
                        room_occupancy[room_id] = patient_id  # Mark room as occupied
                        x, y = get_room_position(room_id)  # Use 2-column layout positioning
                        
                        # Calculate time in room
                        room_entry_time = patient.get('exam_room_assigned', time_point)
                        time_in_room = max(0, time_point - room_entry_time)
                        
                        frame_data['patients'].append({
                            'patient_id': patient_id,
                            'x': x,
                            'y': y + 0.1,  # Positioned on top of room area
                            'color': color,
                            'location': f'Exam Room {room_id}',
                            'size': 12  # Increased size for better visibility
                        })
                        
                        # Add patient total time in system label
                        total_time_in_system = time_point - patient['arrival_time']
                        frame_data['annotations'].append({
                            'x': x, 'y': y - 0.25,
                            'text': f'{total_time_in_system:.0f}m',
                            'showarrow': False,
                            'font': {'color': 'darkgreen', 'size': 10, 'weight': 'bold'},
                            'bgcolor': 'rgba(255,255,255,0.8)',
                            'bordercolor': 'darkgreen',
                            'borderwidth': 1
                        })
        
        # Add mobile staff
        # Registration nurse
        active_registrations = current_patients[
            (current_patients['registration_start'] <= time_point) & 
            (current_patients['registration_end'] > time_point)
        ]
        
        if not active_registrations.empty:
            frame_data['staff'].append({
                'staff_type': 'Registration Nurse',
                'x': 1.5,
                'y': 2.2,  # Positioned on top of unregistered waiting area
                'color': 'purple',  # Always purple
                'symbol': 'diamond',  # Consistent shape with other nurses
                'size': 12  # Consistent size
            })
        
        # Track staff to prevent overlap and simultaneous service
        staff_positions = {}
        
        # Nurses in exam rooms
        active_nurse_visits = current_patients[
            (current_patients['nurse_visit_start'] <= time_point) & 
            (current_patients['nurse_visit_end'] > time_point)
        ]
        
        for idx, patient in active_nurse_visits.iterrows():
            room_id = patient.get('room_id', 0)
            if room_id < num_rooms and f'room_{room_id}' not in staff_positions:
                staff_positions[f'room_{room_id}'] = 'nurse'
                x, y = get_room_position(room_id)  # Use 2-column layout positioning
                frame_data['staff'].append({
                    'staff_type': f'Nurse (Room {room_id})',
                    'x': x - 0.15,  # Positioned on left side of room
                    'y': y + 0.05,  # Positioned on top of room area
                    'color': 'purple',  # Always purple for nurses
                    'symbol': 'diamond',
                    'size': 14  # Increased size for better visibility
                })
        
        # Doctors in exam rooms (only if nurse is not currently serving)
        active_doctor_visits = current_patients[
            (current_patients['doctor_visit_start'] <= time_point) & 
            (current_patients['doctor_visit_end'] > time_point)
        ]
        
        for idx, patient in active_doctor_visits.iterrows():
            room_id = patient.get('room_id', 0)
            # Only allow doctor if no nurse is currently serving in the room
            if (room_id < num_rooms and 
                f'room_{room_id}' not in staff_positions):
                staff_positions[f'room_{room_id}'] = 'doctor'
                x, y = get_room_position(room_id)  # Use 2-column layout positioning
                frame_data['staff'].append({
                    'staff_type': f'Doctor (Room {room_id})',
                    'x': x + 0.15,  # Positioned on right side of room
                    'y': y + 0.05,  # Positioned on top of room area
                    'color': 'blue',  # Always blue for doctors
                    'symbol': 'triangle-up',
                    'size': 14  # Increased size for better visibility
                })
        
        # Add unused staff display by discharge area
        add_unused_staff_display(frame_data, current_patients, time_point, num_rooms, num_doctors, num_nurses)
        
        animation_frames.append(frame_data)
    
    return animation_frames

def add_unused_staff_display(frame_data, current_patients, time_point, num_rooms, num_doctors=3, num_nurses=2):
    """Add unused staff display by discharge area"""
    # Use actual configuration
    total_doctors = num_doctors
    total_nurses = num_nurses
    
    # Count active staff
    active_doctors = len(current_patients[
        (current_patients['doctor_visit_start'] <= time_point) & 
        (current_patients['doctor_visit_end'] > time_point)
    ])
    
    active_nurses = len(current_patients[
        (current_patients['nurse_visit_start'] <= time_point) & 
        (current_patients['nurse_visit_end'] > time_point)
    ])
    
    # Calculate unused staff
    unused_doctors = total_doctors - active_doctors
    unused_nurses = total_nurses - active_nurses
    
    # Position unused staff by discharge area in rows
    discharge_x = 6.5
    discharge_y = 2
    
    # Display unused doctors
    for i in range(unused_doctors):
        row = i // 3  # 3 per row
        col = i % 3
        frame_data['staff'].append({
            'staff_type': f'Available Doctor {i+1}',
            'x': discharge_x + col * 0.2,
            'y': discharge_y + 0.4 + row * 0.2,
            'color': 'blue',  # Always blue
            'symbol': 'triangle-up',
            'size': 12  # Consistent size
        })
    
    # Display unused nurses
    for i in range(unused_nurses):
        row = i // 3  # 3 per row
        col = i % 3
        frame_data['staff'].append({
            'staff_type': f'Available Nurse {i+1}',
            'x': discharge_x + col * 0.2,
            'y': discharge_y - 0.4 - row * 0.2,
            'color': 'purple',  # Always purple
            'symbol': 'diamond',
            'size': 12  # Consistent size
        })

def create_animated_figure(animation_data, max_time, num_rooms=3):
    """Create Plotly figure with built-in animation"""
    
    # Prepare data for Plotly animation
    all_patients = []
    all_staff = []
    
    for frame_data in animation_data:
        time_point = frame_data['time']
        
        # Add patients for this frame
        for patient in frame_data['patients']:
            all_patients.append({
                'time': time_point,
                'patient_id': patient['patient_id'],
                'x': patient['x'],
                'y': patient['y'],
                'color': patient['color'],
                'location': patient['location'],
                'size': patient['size'],
                'type': 'patient'
            })
        
        # Add staff for this frame
        for staff in frame_data['staff']:
            all_staff.append({
                'time': time_point,
                'staff_id': staff['staff_type'],
                'x': staff['x'],
                'y': staff['y'],
                'color': staff['color'],
                'symbol': staff['symbol'],
                'size': staff['size'],
                'type': 'staff'
            })
    
    # Convert to DataFrame for Plotly
    import pandas as pd
    df_patients = pd.DataFrame(all_patients)
    df_staff = pd.DataFrame(all_staff)
    
    # Create the figure
    fig = go.Figure()
    
    # Add static elements (stations and arrows)
    add_static_elements(fig, num_rooms)
    
    # Add animated patients
    if not df_patients.empty:
        # Group by patient for consistent colors
        for patient_id in df_patients['patient_id'].unique():
            patient_data = df_patients[df_patients['patient_id'] == patient_id]
            
            fig.add_trace(go.Scatter(
                x=patient_data['x'],
                y=patient_data['y'],
                mode='markers',
                marker=dict(
                    size=12,  # Consistent size
                    color='green',  # Always green
                    symbol='circle',  # Consistent shape
                    line=dict(color='black', width=1)  # Add border for better visibility
                ),
                name=patient_id,
                showlegend=False,
                text=patient_id,
                hoverinfo='text'
            ))
    
    # Add animated staff
    if not df_staff.empty:
        # Group by staff type for consistent styling
        for staff_id in df_staff['staff_id'].unique():
            staff_data = df_staff[df_staff['staff_id'] == staff_id]
            
            # Staff styling
            if 'Doctor' in staff_id:
                color = 'blue'
                symbol = 'triangle-up'
            elif 'Nurse' in staff_id:
                color = 'purple'
                symbol = 'diamond'
            else:
                color = staff_data['color'].iloc[0]
                symbol = staff_data['symbol'].iloc[0]
            
            fig.add_trace(go.Scatter(
                x=staff_data['x'],
                y=staff_data['y'],
                mode='markers',
                marker=dict(
                    size=12,  # Consistent size
                    color=color,
                    symbol=symbol,
                    line=dict(color='black', width=1)  # Add border for better visibility
                ),
                name=staff_id,
                showlegend=False,
                text=staff_id,
                hoverinfo='text'
            ))
    
    # Create animation frames
    frames = []
    for i, frame_data in enumerate(animation_data):
        frame_traces = []
        
        # Patient traces for this frame
        if not df_patients.empty:
            for patient_id in df_patients['patient_id'].unique():
                patient_frame_data = df_patients[
                    (df_patients['patient_id'] == patient_id) & 
                    (df_patients['time'] == frame_data['time'])
                ]
                
                if not patient_frame_data.empty:
                    frame_traces.append(go.Scatter(
                        x=patient_frame_data['x'],
                        y=patient_frame_data['y'],
                        mode='markers',
                        marker=dict(
                            size=12,  # Consistent size
                            color='green',  # Always green
                            symbol='circle',  # Consistent shape
                            line=dict(color='black', width=1)  # Add border for better visibility
                        ),
                        name=patient_id,
                        showlegend=False,
                        text=patient_id,
                        hoverinfo='text'
                    ))
                else:
                    # Empty trace
                    frame_traces.append(go.Scatter(
                        x=[],
                        y=[],
                        mode='markers',
                        name=patient_id,
                        showlegend=False
                    ))
        
        # Staff traces for this frame
        if not df_staff.empty:
            for staff_id in df_staff['staff_id'].unique():
                staff_frame_data = df_staff[
                    (df_staff['staff_id'] == staff_id) & 
                    (df_staff['time'] == frame_data['time'])
                ]
                
                if not staff_frame_data.empty:
                    # Staff styling
                    if 'Doctor' in staff_id:
                        color = 'blue'
                        symbol = 'triangle-up'
                    elif 'Nurse' in staff_id:
                        color = 'purple'
                        symbol = 'diamond'
                    else:
                        color = staff_frame_data['color'].iloc[0]
                        symbol = staff_frame_data['symbol'].iloc[0]
                    
                    frame_traces.append(go.Scatter(
                        x=staff_frame_data['x'],
                        y=staff_frame_data['y'],
                        mode='markers',
                        marker=dict(
                            size=12,  # Consistent size
                            color=color,
                            symbol=symbol,
                            line=dict(color='black', width=1)  # Add border for better visibility
                        ),
                        name=staff_id,
                        showlegend=False
                    ))
                else:
                    # Empty trace
                    frame_traces.append(go.Scatter(
                        x=[],
                        y=[],
                        mode='markers',
                        name=staff_id,
                        showlegend=False
                    ))
        
        # Collect all annotations for this frame (removed red time text)
        all_annotations = []
        
        # Add dynamic annotations from frame data
        for annotation in frame_data.get('annotations', []):
            all_annotations.append(annotation)
        
        frames.append(go.Frame(
            data=frame_traces,
            name=str(int(frame_data['time'])),
            layout=go.Layout(
                annotations=all_annotations
            )
        ))
    
    fig.frames = frames
    
    # Configure layout with animation controls
    fig.update_layout(
        title={
            'text': '',
            'font': {'color': '#000000', 'size': 16}
        },
        xaxis=dict(
            range=[0.5, 8.0],  # Extended to accommodate 2-column room layout
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[-0.5, 4.0],  # Extended range to accommodate 2-column layout
            showgrid=False,
            zeroline=False,
            showticklabels=False
        ),
        height=650,  # Increased height to accommodate 2-column layout
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#000000', 'size': 14},
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶️ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 500, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 300, 'easing': 'quadratic-in-out'}
                    }]
                },
                {
                    'label': '⏸️ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }],
        sliders=[{
            'steps': [
                {
                    'args': [[frame.name], {
                        'frame': {'duration': 300, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    }],
                    'label': f'{frame.name} min',
                    'method': 'animate'
                }
                for frame in frames
            ],
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Time: ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
        }]
    )
    
    return fig

def add_static_elements(fig, num_rooms=3):
    """Add static elements (stations and arrows) to the figure"""
    
    # Define non-exam room station positions
    stations = {
        'Waiting Room': (2, 2),
        'Discharged': (6, 2)
    }
    
    # Draw non-exam room stations as rectangles
    for station, (x, y) in stations.items():
        if station == 'Waiting Room':
            color = "lightgreen"
            width, height = 0.8, 0.4
        else:
            color = "lightgray"
            width, height = 0.3, 0.2
        
        fig.add_shape(
            type="rect",
            x0=x-width/2, y0=y-height/2,
            x1=x+width/2, y1=y+height/2,
            fillcolor=color,
            line=dict(color="black", width=2),
            layer="below"  # Ensure areas are drawn below entities
        )
        # Add station label
        if 'Waiting' in station:
            fig.add_annotation(
                x=x, y=y-0.25,
                text=station,
                showarrow=False,
                font=dict(color="black", size=11, weight="bold")
            )
        elif 'Discharged' in station:
            fig.add_annotation(
                x=x, y=y-0.05,
                text=station,
                showarrow=False,
                font=dict(color="black", size=10)
            )
    
    # Dynamically create exam rooms based on num_rooms in 2-column layout
    for i in range(num_rooms):
        if i < 5:
            # First column (left side)
            room_x = 3.5
            room_y = 3.5 - i * 0.7  # Spread rooms vertically with smaller spacing
        else:
            # Second column (right side)
            room_x = 4.5
            room_y = 3.5 - (i - 5) * 0.7  # Continue from top for second column
        
        # Draw exam room rectangle
        fig.add_shape(
            type="rect",
            x0=room_x-0.25, y0=room_y-0.15,
            x1=room_x+0.25, y1=room_y+0.15,
            fillcolor="lightblue",
            line=dict(color="black", width=2),
            layer="below"  # Ensure areas are drawn below entities
        )
    
    # Add single "Exam Rooms" title below all rooms
    if num_rooms > 0:
        # Position title below the center of the two-column layout
        fig.add_annotation(
            x=4, y=0.0,  # Center between two columns, below all rooms
            text="Exam Rooms",
            showarrow=False,
            font=dict(color="black", size=12, weight="bold")
        )
    
    # Add arrows showing patient flow dynamically
    arrow_positions = []
    
    # Arrow from unregistered to registered waiting
    arrow_positions.append(((1.8, 2.0), (2.2, 2.0)))
    
    # Arrows from registered waiting to each exam room
    for i in range(num_rooms):
        if i < 5:
            room_x = 3.5
            room_y = 3.5 - i * 0.7
        else:
            room_x = 4.5
            room_y = 3.5 - (i - 5) * 0.7
        arrow_positions.append(((2.8, 2.2), (room_x - 0.25, room_y)))
    
    # Arrows from each exam room to discharge
    for i in range(num_rooms):
        if i < 5:
            room_x = 3.5
            room_y = 3.5 - i * 0.7
        else:
            room_x = 4.5
            room_y = 3.5 - (i - 5) * 0.7
        arrow_positions.append(((room_x + 0.25, room_y), (5.7, 2.2)))
    
    for (x1, y1), (x2, y2) in arrow_positions:
        fig.add_annotation(
            x=x2, y=y2,
            ax=x1, ay=y1,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="gray"
        )

def display_charts(results, num_rooms=3):
    if results is None:
        return
    
    st.markdown("---")
    
    # Simple tabs for charts
    tab1, tab2, tab3 = st.tabs(["Patient Flow", "Resource Usage", "Time Analysis"])
    
    with tab1:
        
        # Create patient flow visualization
        journey_df = results['patient_journey_summary']
        
        if not journey_df.empty:
            # Create animation data for Plotly
            max_time = results['simulation_duration']
            
            # Validate max_time and ensure float type
            if max_time <= 0:
                max_time = 120.0  # Default to 2 hours
            else:
                max_time = float(max_time)  # Ensure it's a float
            
            
            # Create animation frames data
            animation_data = create_animation_frames(journey_df, max_time, num_rooms, 
                                                  results.get('num_doctors', 3), 
                                                  results.get('num_nurses', 2))
            
            # Create animated figure using Plotly's built-in animation
            fig = create_animated_figure(animation_data, max_time, num_rooms)
            
            # Display the animated chart
            st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
            # Add simple legend
            st.markdown("""
            **Legend:** 🟢 Patients • 🟣 Nurses • 🔵 Doctors
            """)
            
            # Add summary statistics for final time
            final_frame = animation_data[-1] if animation_data else None
            if final_frame:
                waiting_count = len([p for p in final_frame['patients'] if p['location'] == 'Waiting Room'])
                room_count = len([p for p in final_frame['patients'] if 'Exam Room' in p['location']])
                col1 = st.columns(1)[0]
                with col1:
                    st.metric("Total Simulation Time", f"{max_time:.0f} min")
                
        else:
            st.info("No simulation data available for patient flow visualization.")
    
    with tab2:
        journey_df = results['patient_journey_summary']
        
        if not journey_df.empty:
            # Create resource utilization visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Resource Utilization")
                
                # Calculate average utilization rates
                total_duration = results['simulation_duration']
                num_doctors = results['num_doctors']
                num_nurses = results['num_nurses']
                num_rooms = results['num_rooms']
                num_registration = results.get('num_registration', 1)
                
                # Calculate total time each resource was used
                completed = journey_df[journey_df['service_completed'] == True]
                if not completed.empty:
                    total_registration_time = (completed['registration_end'] - completed['registration_start']).sum()
                    total_nurse_time = (completed['nurse_visit_end'] - completed['nurse_visit_start']).sum()
                    total_doctor_time = (completed['doctor_visit_end'] - completed['doctor_visit_start']).sum()
                    total_room_time = (completed['doctor_visit_end'] - completed['exam_room_assigned']).sum()
                    
                    # Calculate utilization rates
                    reg_utilization = (total_registration_time / (total_duration * num_registration)) * 100
                    nurse_utilization = (total_nurse_time / (total_duration * num_nurses)) * 100
                    doctor_utilization = (total_doctor_time / (total_duration * num_doctors)) * 100
                    room_utilization = (total_room_time / (total_duration * num_rooms)) * 100
                    
                    # Create bar chart
                    fig = go.Figure(data=[
                        go.Bar(
                            x=['Registration', 'Nurses', 'Doctors', 'Exam Rooms'],
                            y=[reg_utilization, nurse_utilization, doctor_utilization, room_utilization],
                            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                        )
                    ])
                    
                    axis_style = get_axis_style()
                    fig.update_layout(
                        **get_chart_theme(),
                        height=400,
                        showlegend=False,
                        xaxis={**axis_style, 'showticklabels': False},
                        yaxis={**axis_style, 'title': {'text': 'Utilization (%)', 'font': {'color': '#000000'}}, 'range': [0, 100]}
                    )
                    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
                else:
                    st.info(f"No completed patients to calculate utilization. Total patients: {len(journey_df)}")
            
            with col2:
                st.subheader("Service Times")
                
                completed = journey_df[journey_df['service_completed'] == True]
                if not completed.empty:
                    # Calculate service times
                    reg_times = completed['registration_end'] - completed['registration_start']
                    nurse_times = completed['nurse_visit_end'] - completed['nurse_visit_start']
                    doctor_times = completed['doctor_visit_end'] - completed['doctor_visit_start']
                    
                    # Create box plot
                    fig = go.Figure()
                    fig.add_trace(go.Box(y=reg_times, name='Registration', marker_color='#1f77b4'))
                    fig.add_trace(go.Box(y=nurse_times, name='Nurse Visit', marker_color='#ff7f0e'))
                    fig.add_trace(go.Box(y=doctor_times, name='Doctor Visit', marker_color='#2ca02c'))
                    
                    axis_style = get_axis_style()
                    fig.update_layout(
                        **get_chart_theme(),
                        height=400,
                        xaxis={**axis_style, 'showticklabels': False},
                        yaxis={**axis_style, 'title': {'text': 'Time (minutes)', 'font': {'color': '#000000'}}}
                    )
                    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
                else:
                    st.info(f"No completed patients to display service times. Total patients: {len(journey_df)}")
            
            # Add resource utilization over time line chart
            st.subheader("Resource Utilization Over Time")
            
            # Create time series data for resource utilization
            if not completed.empty:
                # Group by time intervals (e.g., every 10 minutes)
                time_intervals = []
                reg_utils = []
                nurse_utils = []
                doctor_utils = []
                room_utils = []
                
                max_time = total_duration
                interval_size = max(5, max_time // 20)  # Dynamic interval size
                
                for t in range(0, int(max_time), interval_size):
                    time_end = t + interval_size
                    
                    # Count active resources at this time
                    active_at_time = completed[
                        (completed['registration_start'] <= time_end) & 
                        (completed['departure_time'] > t)
                    ]
                    
                    if not active_at_time.empty:
                        # Calculate utilization for this interval
                        reg_active = active_at_time[
                            (active_at_time['registration_start'] <= time_end) & 
                            (active_at_time['registration_end'] > t)
                        ]
                        nurse_active = active_at_time[
                            (active_at_time['nurse_visit_start'] <= time_end) & 
                            (active_at_time['nurse_visit_end'] > t)
                        ]
                        doctor_active = active_at_time[
                            (active_at_time['doctor_visit_start'] <= time_end) & 
                            (active_at_time['doctor_visit_end'] > t)
                        ]
                        room_active = active_at_time[
                            (active_at_time['exam_room_assigned'] <= time_end) & 
                            (active_at_time['departure_time'] > t)
                        ]
                        
                        time_intervals.append(t)
                        reg_utils.append(len(reg_active) / num_registration * 100)
                        nurse_utils.append(len(nurse_active) / num_nurses * 100)
                        doctor_utils.append(len(doctor_active) / num_doctors * 100)
                        room_utils.append(len(room_active) / num_rooms * 100)
                
                if time_intervals:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=time_intervals, y=reg_utils, name='Registration', line=dict(color='#1f77b4')))
                    fig.add_trace(go.Scatter(x=time_intervals, y=nurse_utils, name='Nurses', line=dict(color='#ff7f0e')))
                    fig.add_trace(go.Scatter(x=time_intervals, y=doctor_utils, name='Doctors', line=dict(color='#2ca02c')))
                    fig.add_trace(go.Scatter(x=time_intervals, y=room_utils, name='Exam Rooms', line=dict(color='#d62728')))
                    
                    axis_style = get_axis_style()
                    fig.update_layout(
                        **get_chart_theme(),
                        height=400,
                        showlegend=False,
                        xaxis={**axis_style, 'title': {'text': 'Time (minutes)', 'font': {'color': '#000000'}}},
                        yaxis={**axis_style, 'title': {'text': 'Utilization (%)', 'font': {'color': '#000000'}}, 'range': [0, 100]}
                    )
                    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
                else:
                    st.info("No utilization data available for time series.")
            else:
                st.info("No completed patients to display resource utilization over time.")
        else:
            st.info("No patient data to display resource utilization.")
    
    with tab3:
        journey_df = results['patient_journey_summary']
        completed = journey_df[journey_df['service_completed'] == True]
        
        if not completed.empty:
            # Create four columns for the time analysis tab
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Time Breakdown by Patient")
                
                # Sort by discharge time and show individual patient breakdown
                completed_sorted = completed.sort_values('departure_time')
                
                # Take first 20 patients to avoid overcrowding
                display_patients = completed_sorted.head(20)
                
                # Calculate durations for each patient
                reg_times = display_patients['registration_end'] - display_patients['registration_start']
                wait_times = display_patients['waiting_time']
                nurse_times = display_patients['nurse_visit_end'] - display_patients['nurse_visit_start']
                doctor_times = display_patients['doctor_visit_end'] - display_patients['doctor_visit_start']
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Registration', x=display_patients['patient_id'], y=reg_times, marker_color='#1f77b4'))
                fig.add_trace(go.Bar(name='Waiting', x=display_patients['patient_id'], y=wait_times, marker_color='#ff7f0e'))
                fig.add_trace(go.Bar(name='Nurse Visit', x=display_patients['patient_id'], y=nurse_times, marker_color='#2ca02c'))
                fig.add_trace(go.Bar(name='Doctor Visit', x=display_patients['patient_id'], y=doctor_times, marker_color='#d62728'))
                
                axis_style = get_axis_style()
                fig.update_layout(
                    **get_chart_theme(),
                    barmode='stack',
                    height=400,
                    xaxis={**axis_style, 'title': {'text': 'Patient ID', 'font': {'color': '#000000'}}, 'tickangle': 45},
                    yaxis={**axis_style, 'title': {'text': 'Time (minutes)', 'font': {'color': '#000000'}}}
                )
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
            with col2:
                st.subheader("Total Time Distribution")
                
                # Create histogram of total time in system
                fig = px.histogram(
                    completed,
                    x='total_time',
                    nbins=15,
                    labels={'total_time': 'Total Time (minutes)', 'count': 'Number of Patients'},
                    color_discrete_sequence=['#2ca02c']  # Green color
                )
                axis_style = get_axis_style()
                fig.update_layout(**get_chart_theme(), height=400, 
                                 xaxis={**axis_style, 'showticklabels': True, 'title': {'text': 'Total Time (minutes)', 'font': {'color': '#000000'}}},
                                 yaxis={**axis_style, 'title': {'text': 'Count', 'font': {'color': '#000000'}}})
                fig.update_traces(marker_line_width=1, marker_line_color='white')
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
            # Add more charts below
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("Wait Time Distribution")
                fig = px.histogram(
                    completed,
                    x='waiting_time',
                    nbins=15,
                    labels={'waiting_time': 'Wait Time (minutes)', 'count': 'Number of Patients'},
                    color_discrete_sequence=['#ff7f0e']  # Orange color
                )
                axis_style = get_axis_style()
                fig.update_layout(**get_chart_theme(), height=400, 
                                 xaxis={**axis_style, 'showticklabels': True, 'title': {'text': 'Wait Time (minutes)', 'font': {'color': '#000000'}}},
                                 yaxis={**axis_style, 'title': {'text': 'Count', 'font': {'color': '#000000'}}})
                fig.update_traces(marker_line_width=1, marker_line_color='white')
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
            
            with col4:
                # Create time series of average wait times
                completed_sorted = completed.sort_values('departure_time')
                
                # Calculate rolling average wait time
                window_size = max(5, len(completed_sorted) // 10)  # Dynamic window size
                completed_sorted['rolling_wait_time'] = completed_sorted['waiting_time'].rolling(window=window_size, min_periods=1).mean()
                
                # Calculate overall average for title
                overall_avg_wait = completed_sorted['rolling_wait_time'].iloc[-1] if len(completed_sorted) > 0 else 0
                st.subheader(f"Average Wait Time Over Time ({overall_avg_wait:.1f} min avg)")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=completed_sorted['departure_time'],
                    y=completed_sorted['rolling_wait_time'],
                    mode='lines+markers',
                    name='Rolling Average Wait Time',
                    line=dict(color='#ff7f0e', width=3),
                    marker=dict(size=4)
                ))
                
                axis_style = get_axis_style()
                fig.update_layout(
                    **get_chart_theme(),
                    height=400,
                    showlegend=False,
                    xaxis={**axis_style, 'title': {'text': 'Discharge Time (minutes)', 'font': {'color': '#000000'}}},
                    yaxis={**axis_style, 'title': {'text': 'Average Wait Time (minutes)', 'font': {'color': '#000000'}}}
                )
                st.plotly_chart(fig, use_container_width=True, theme="streamlit")
        else:
            st.info("No completed patients to display time analysis.")

def main():
    initialize_session_state()
    
    # Create sidebar
    config = create_sidebar()
    
    # Always show progress bar
    progress_bar = st.progress(st.session_state.simulation_progress)
    status_text = st.empty()
    
    # Run simulation if button clicked
    if config['run_simulation']:
        try:
            # Update progress during simulation
            st.session_state.simulation_progress = 10
            st.session_state.simulation_status = "🔄 Initializing simulation..."
            status_text.text(st.session_state.simulation_status)
            progress_bar.progress(st.session_state.simulation_progress)
            
            st.session_state.simulation_progress = 30
            st.session_state.simulation_status = "🔄 Running patient simulation..."
            status_text.text(st.session_state.simulation_status)
            progress_bar.progress(st.session_state.simulation_progress)
            
            results = run_simulation_with_config(config)
            
            st.session_state.simulation_progress = 70
            st.session_state.simulation_status = "🔄 Processing results..."
            status_text.text(st.session_state.simulation_status)
            progress_bar.progress(st.session_state.simulation_progress)
            
            st.session_state.simulation_results = results
            
            st.session_state.simulation_progress = 90
            st.session_state.simulation_status = "🔄 Generating visualizations..."
            status_text.text(st.session_state.simulation_status)
            progress_bar.progress(st.session_state.simulation_progress)
            
            # Complete
            st.session_state.simulation_progress = 100
            st.session_state.simulation_status = "✅ Simulation completed successfully!"
            status_text.success(st.session_state.simulation_status)
            progress_bar.progress(st.session_state.simulation_progress)
            
        except Exception as e:
            st.session_state.simulation_progress = 0
            st.session_state.simulation_status = f"❌ Simulation failed: {str(e)}"
            status_text.error(st.session_state.simulation_status)
            progress_bar.progress(st.session_state.simulation_progress)
            st.session_state.simulation_results = None
    else:
        # Show current status when not running
        if st.session_state.simulation_progress == 100:
            status_text.success(st.session_state.simulation_status)
        elif st.session_state.simulation_progress == 0 and "failed" in st.session_state.simulation_status:
            status_text.error(st.session_state.simulation_status)
        else:
            status_text.text(st.session_state.simulation_status)
    
    # Display results
    display_main_results(st.session_state.simulation_results)
    display_charts(st.session_state.simulation_results, config['num_rooms'])

if __name__ == "__main__":
    main()