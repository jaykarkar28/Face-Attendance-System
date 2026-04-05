# 🧑‍💼 Smart Face Attendance System

A modern, fast, and completely offline real-time facial recognition attendance system built using **OpenCV**, **Scikit-Learn (KNN)**, and a **Streamlit** dashboard.

## ✨ Features

- **Rich Streamlit Dashboard**: A beautifully designed, glassmorphic UI dashboard to view and manage all attendance data.
- **Fast Face Registration**: Quickly add new faces to the database via webcam. The system will auto-capture 100 frames seamlessly.
- **Live Facial Recognition**: Utilizes a robust K-Nearest Neighbors (KNN) classification model to instantly recognize registered faces and mark their attendance.
- **Dynamic Analytics**: Includes daily data logs, unique scanner identification, and timeline bar charts tracking presence.
- **User Management**: An easy admin interface inside the dashboard allows you to view saved face data or delete users out of the system. 

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Face Detection Algorithm**: OpenCV (Haar Cascades)
- **Classification Model**: K-Nearest Neighbors (Scikit-Learn)
- **Data Management**: Pandas & Pickle files

## 🚀 Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/Face-Attendance.git
cd Face-Attendance
```

**2. Create a virtual environment & install dependencies**
```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

**3. Run the Application**
```bash
streamlit run frontend.py
```

## 🖥️ Usage Guide

1. **Dashboard Overview**: Launch the Streamlit server and navigate the sidebar.
2. **Add Faces**: Select `Add Faces` in the sidebar. Type in the person's name. An OpenCV window will pop up. Stare directly at the camera until it captures 100 frames and auto-closes.
3. **Take Attendance**: Select `Take Attendance` from the sidebar and click the Start button. When the camera window pops up, it will actively track recognized faces. Press the **`O`** key (letter O) on your keyboard to formally log the tracked attendance into the system database, or **`Q`** to exit.
4. **View Analytics**: Use the Dashboard calendar to review attendance sheets seamlessly for any day.

## 📂 Project Structure
```text
Face-Attendance/
├── frontend.py        # Streamlit App & Main Dashboard Hub
├── add_faces.py       # Computer Vision Face Registration component 
├── test.py            # AI Face Recognition & Attendance component
├── data/              # Stores KNN embeddings & trained pickle models
├── Attendance/        # Automatically generated CSV reports by Date
└── requirements.txt   # Core Dependencies
```
