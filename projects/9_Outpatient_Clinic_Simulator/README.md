# Outpatient Clinic Simulation Tool

A professional discrete-event simulation application for modeling outpatient clinic operations using SimPy and Streamlit.

## 🎯 Purpose

This tool helps healthcare administrators and researchers:
- **Optimize patient flow** through realistic clinic simulation
- **Analyze resource utilization** for doctors, nurses, and exam rooms
- **Reduce patient wait times** through data-driven insights
- **Visualize clinic operations** with interactive charts and animations

## 🚀 Features

- **Clean Web Interface**: Professional Streamlit dashboard
- **Realistic Patient Journey**: Registration → Exam Room → Nurse → Doctor → Discharge
- **Interactive Visualization**: Real-time patient flow animation
- **Comprehensive Analytics**: KPIs, time distributions, and resource utilization
- **Performance Optimized**: Streamlit caching for responsive UI
- **Docker Ready**: Containerized for easy deployment
- **Cloud Deployment**: Ready for Streamlit Cloud, Google Cloud Run, or Railway

## 📋 Project Structure

```
outpatient-clinic-sim/
├── app.py                        # Main Streamlit web application
├── simulation.py                 # Core clinic model and resources
├── realistic_patient_journey.py  # Patient flow simulation engine
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container configuration
├── .dockerignore                 # Docker build optimization
├── .gitignore                    # Git version control
└── README.md                     # This file
```

## 🛠️ Installation

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd outpatient-clinic-sim
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**:
   Open your browser to `http://localhost:8501`

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker build -t clinic-sim .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8501:8501 clinic-sim
   ```

3. **Access the app**:
   Open your browser to `http://localhost:8501`

## 📊 How to Use

### Control Panel
Configure parameters in the sidebar:
- **Resources**: Doctors (1-8), Nurses (1-6), Exam Rooms (1-10), Registration Staff (1-4)
- **Processing Times**: Registration, Nurse Visit, Doctor Visit (in minutes)
- **Patient Arrivals**: Average time between patient arrivals
- **Simulation**: Duration (1-8 hours), Random Seed for reproducibility

### Running Simulation
1. Adjust parameters in the sidebar
2. Click "🚀 Run Simulation" 
3. Watch the progress bar as simulation runs
4. Explore results in three tabs:
   - **Patient Flow**: Interactive animation of patient movement
   - **Resource Usage**: Utilization charts and service time analysis
   - **Time Analysis**: Patient journey breakdowns and distributions

### Key Metrics
- **Patients Served**: Total patients who completed their visit
- **Average Wait Time**: Time from arrival to doctor consultation
- **Average Total Time**: Complete visit duration
- **Resource Utilization**: Percentage of time each resource is busy
- **Service Completion Rate**: Percentage of patients who complete their visit

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Easiest)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Click "Deploy"
5. Get a public URL like `https://your-app.streamlit.app`

**Cost**: Free  
**Time**: 5 minutes  
**Best for**: Quick demos and portfolio projects

### Option 2: Google Cloud Run (Recommended)
1. Install Google Cloud CLI
2. Build and push container:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR-PROJECT/clinic-sim
   ```
3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy clinic-sim \
     --image gcr.io/YOUR-PROJECT/clinic-sim \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Cost**: ~$0-5/month (scales to zero)  
**Time**: 20-30 minutes  
**Best for**: Professional deployment with custom domain

### Option 3: Railway
1. Connect GitHub to Railway
2. Deploy directly from repository
3. Automatic HTTPS and custom domains

**Cost**: $5/month  
**Time**: 10 minutes  
**Best for**: Developer-friendly deployment

## 📈 Technical Implementation

### Architecture
- **Simulation Engine**: SimPy discrete-event simulation
- **Web Framework**: Streamlit with session state management
- **Data Processing**: Pandas and NumPy for analytics
- **Visualization**: Plotly for interactive charts and animations
- **Performance**: `@st.cache_data` for responsive UI
- **Deployment**: Docker containerization

### Patient Journey Model
1. **Arrival**: Patient enters waiting room
2. **Registration**: Mobile nurse visits patient for check-in
3. **Exam Room**: Patient moves to available exam room
4. **Nurse Visit**: Nurse performs initial assessment
5. **Doctor Visit**: Doctor consultation and treatment
6. **Discharge**: Patient leaves, room becomes available

### Resource Modeling
- **Doctors**: Limited capacity with queue management
- **Nurses**: Mobile staff serving patients in exam rooms
- **Exam Rooms**: Physical space constraints
- **Registration Staff**: Mobile check-in service

## 🔧 Configuration Details

### Service Time Distributions
- **Registration**: Normal distribution (mean=3, std=0.8 minutes)
- **Nurse Visit**: Normal distribution (mean=8, std=2.0 minutes)
- **Doctor Visit**: Normal distribution (mean=12, std=4.0 minutes)

### Patient Arrival Process
- **Exponential Distribution**: Models random arrival intervals
- **Configurable Rate**: 1-15 minutes between arrivals
- **Realistic Patterns**: Simulates typical clinic flow

### Data Collection
- **Real-time Tracking**: Patient locations and wait times
- **Resource Utilization**: Continuous monitoring of all resources
- **Performance Metrics**: Comprehensive KPI calculation
- **Animation Data**: Frame-by-frame patient movement tracking

## 🛡️ Code Quality

### Performance Optimization
- **Caching**: `@st.cache_data` prevents unnecessary simulation reruns
- **State Management**: Proper use of `st.session_state`
- **Memory Efficient**: Cleanup of large data structures

### Professional Standards
- **Clean Code**: Simplified comments and clear structure
- **Type Hints**: Proper type annotations
- **Error Handling**: Graceful failure management
- **Documentation**: Comprehensive inline documentation

## 📝 Development Notes

### File Purposes
- **app.py**: Main Streamlit interface with caching and state management
- **simulation.py**: Core clinic resources and SimPy environment
- **realistic_patient_journey.py**: Patient flow logic and data collection

### Key Features
- **Two-column exam room layout**: Supports up to 10 rooms
- **Dynamic resource allocation**: Realistic staff movement
- **Comprehensive analytics**: Multiple chart types and KPIs
- **Progress tracking**: Real-time simulation progress bar

## 🤝 Contributing

This is a professional healthcare simulation tool. Contributions welcome:
- Report issues or suggest improvements
- Fork for your own modifications
- Submit pull requests for enhancements

## 📄 License

MIT License - feel free to use for educational and commercial purposes.

---

**Built with Python, SimPy, and Streamlit** | **Optimized for production deployment**