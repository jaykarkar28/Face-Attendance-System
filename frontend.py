import streamlit as st
import pandas as pd
import time
from datetime import datetime
import os
import subprocess
import sys

# ----------------- Configuration & CSS -----------------
st.set_page_config(page_title="Face Attendance System", page_icon="🧑‍💼", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

    /* Global App Background */
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Outfit', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(22, 33, 62, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Header Gradient Text */
    .main-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 0 10px 30px rgba(0, 201, 255, 0.2);
    }

    /* Subheaders */
    h2, h3, .stMarkdown p {
        color: #E2E8F0 !important;
    }

    /* Animated Glowing Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00C9FF, #92FE9D);
        color: #0f3460 !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        border-radius: 12px;
        border: none;
        padding: 0.7rem 0;
        box-shadow: 0 6px 15px rgba(0, 201, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(0, 201, 255, 0.6);
        background: linear-gradient(45deg, #92FE9D, #00C9FF);
    }

    /* Sidebar Navigation Buttons */
    [data-testid="stSidebar"] .stButton>button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #E2E8F0 !important;
        box-shadow: none;
        margin-bottom: 10px;
        text-align: left;
        padding-left: 15px;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: linear-gradient(45deg, #00C9FF, #92FE9D);
        color: #0f3460 !important;
        transform: scale(1.03);
        box-shadow: 0 5px 15px rgba(0, 201, 255, 0.4);
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        background-color: rgba(255,255,255,0.05);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 0.8rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00C9FF;
        box-shadow: 0 0 0 2px rgba(0, 201, 255, 0.5);
    }

    /* Styled Images */
    img {
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        transition: transform 0.3s ease;
    }
    img:hover {
        transform: scale(1.05);
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(22, 33, 62, 0.4);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 201, 255, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        background: linear-gradient(135deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

</style>
""", unsafe_allow_html=True)

# ----------------- UI Layout & Routing -----------------

st.markdown("<h1 class='main-header'>🧑‍💼 Smart Face Attendance System</h1>", unsafe_allow_html=True)

# Navigation Menu Logic
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

st.sidebar.markdown("### 📂 Navigation Menu")

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state.page = "Dashboard"
if st.sidebar.button("🧑‍🏫 Add Faces", use_container_width=True):
    st.session_state.page = "Add Faces"
if st.sidebar.button("🖥️ Take Attendance", use_container_width=True):
    st.session_state.page = "Take Attendance"
if st.sidebar.button("👥 View Faces", use_container_width=True):
    st.session_state.page = "View Faces"

choice = st.session_state.page

st.sidebar.markdown("---")
st.sidebar.info("A Python-based Real-time Attendance tracking system powered by OpenCV and Streamlit.")

# Ensure we use the exact python executable running the streamlit server
py_executable = sys.executable

if choice == "Dashboard":
    st.markdown("<h2 style='text-align: center; color: #E2E8F0; margin-bottom: 30px;'>📊 Activity Dashboard</h2>", unsafe_allow_html=True)
    
    # Date Selection Calendar
    selected_date = st.date_input("📅 Select a Date to View Attendance", value=datetime.today())
    formated_date = selected_date.strftime("%d-%m-%Y")
    
    file_path = f"Attendance/Attendance_{formated_date}.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # Calculate KPIs
        total_scans = len(df)
        unique_users = df['NAME'].nunique() if 'NAME' in df.columns else 0
        latest_scan = df['TIME'].iloc[-1] if not df.empty and 'TIME' in df.columns else "--:--:--"
        
        # Top Metrics
        # Space them into three columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Total Attendees", unique_users)
        with col2:
            st.metric("📝 Total Scans", total_scans)
        with col3:
            st.metric("🕒 Latest Scan", latest_scan)
            
        st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
        
        # Detailed Analytics
        col_list, col_chart = st.columns([1, 1])
        
        with col_list:
            st.markdown("<h3 style='color: #92FE9D;'>📌 Detailed Log</h3>", unsafe_allow_html=True)
            # Display DataFrame grouped by name to combine multiple check-ins
            if 'NAME' in df.columns and 'TIME' in df.columns:
                df_grouped = df.groupby('NAME').agg({
                    'TIME': lambda x: ', '.join(map(str, x))
                }).reset_index()
                df_grouped.columns = ['Name', 'Check-in Times']
                st.dataframe(df_grouped, hide_index=True, use_container_width=True)
            else:
                st.dataframe(df, hide_index=True, use_container_width=True)
            
        with col_chart:
            st.markdown("<h3 style='color: #00C9FF;'>📈 Scans per Person</h3>", unsafe_allow_html=True)
            if 'NAME' in df.columns:
                scan_counts = df['NAME'].value_counts().reset_index()
                scan_counts.columns = ['Name', 'Check-ins']
                st.bar_chart(scan_counts.set_index('Name'), color="#00C9FF")
            else:
                st.info("Chart data unavailable")
    else:
        st.warning(f"Not any attendance is taken on {formated_date}.")
        st.info("💡 Go to 'Take Attendance' from the sidebar and mark some attendance to bring this dashboard to life!")

elif choice == "Add Faces":
    st.subheader("🧑‍🏫 Add a New Person")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("Register a new user's face into the system database.")
        new_name = st.text_input("Enter Full Name:")
        
        if st.button("Start Camera & Register"):
            if new_name.strip() == "":
                st.error("Please enter a valid name first!")
            else:
                with st.spinner(f"Opening camera to register {new_name}... Please wait."):
                    # Run the external add_faces.py file
                    try:
                        subprocess.run([py_executable, "add_faces.py", new_name], check=True)
                        st.success(f"🎉 Successfully ran face registration script for **{new_name}**!")
                    except subprocess.CalledProcessError as e:
                        st.error(f"An error occurred while running the script.")

    with col2:
        st.markdown(
            "> **Instructions:**\n"
            "1. Enter your full name.\n"
            "2. Click the register button.\n"
            "3. A separate pop-up camera window will open.\n"
            "4. Stare at your webcam until 100 face samples are gathered.\n"
            "5. The pop-up window will automatically close."
        )

elif choice == "Take Attendance":
    st.subheader("🖥️ Real-time Attendance Recognition")
    col1, col2 = st.columns([1,1])
    with col1:
        st.write("Launch the recognition model to take real-time attendance.")
        if st.button("Start AI Recognition"):
            with st.spinner("Starting AI Recognition camera window... Please wait."):
                # Run the external test.py file
                try:
                    subprocess.run([py_executable, "test.py"], check=True)
                    st.success("Recognition module closed successfully.")
                except subprocess.CalledProcessError as e:
                    st.error("An error occurred while running the recognition script.")
    with col2:
        st.markdown(
            "> **Controls:**\n"
            "- A separate camera window will open.\n"
            "- Press **'O'** (letter o) in the camera window to mark your attendance.\n"
            "- Press **'Q'** in the camera window when you are done."
        )

elif choice == "View Faces":
    st.subheader("👥 Registered Users")
    st.write("Here are the users currently registered in the database:")
    
    import pickle
    import cv2
    import numpy as np
    
    if os.path.exists("data/names.pkl") and os.path.exists("data/faces_data.pkl"):
        try:
            with open("data/names.pkl", "rb") as f:
                names = pickle.load(f)
            with open("data/faces_data.pkl", "rb") as f:
                faces = pickle.load(f)
                
            seen_names = set()
            unique_users = []
            user_faces = []
            
            # Extract the first face for each new name encountered
            for i, name in enumerate(names):
                if name not in seen_names:
                    seen_names.add(name)
                    unique_users.append(name)
                    try:
                        face_img = faces[i].reshape(50, 50, -1) 
                        if face_img.shape[2] == 3:
                            face_img = cv2.cvtColor(face_img.astype(np.uint8), cv2.COLOR_BGR2RGB)
                        face_img_large = cv2.resize(face_img.astype(np.uint8), (150, 150), interpolation=cv2.INTER_NEAREST)
                        user_faces.append(face_img_large)
                    except Exception as e:
                        user_faces.append(None)
                        
            if len(unique_users) > 0:
                cols = st.columns(4)
                for idx, (name, face_img) in enumerate(zip(unique_users, user_faces)):
                    with cols[idx % 4]:
                        if face_img is not None:
                            st.image(face_img, caption=name)
                        else:
                            st.error(f"Image error for {name}")
                        
                        # Add Delete Button for each user
                        if st.button(f"🗑️ Delete {name}", key=f"del_{name}"):
                            try:
                                names_np = np.array(names)
                                mask = names_np != name
                                
                                new_names = names_np[mask].tolist()
                                new_faces = faces[mask]
                                
                                # Write updated data back to pickle files
                                with open("data/names.pkl", "wb") as f_out:
                                    pickle.dump(new_names, f_out)
                                with open("data/faces_data.pkl", "wb") as f_out:
                                    pickle.dump(new_faces, f_out)
                                    
                                st.success(f"Deleted {name} successfully!")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting {name}: {e}")
            else:
                st.info("No valid face data found. The database might be empty.")
                
        except Exception as e:
            st.error(f"An error occurred while loading data: {e}")
    else:
        st.warning("No face data found. Please register users in the 'Add Faces' tab first.")
