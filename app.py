import streamlit as st
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="MedGuard AI", page_icon="🏥", layout="wide")

# Simulation of a database
if 'db' not in st.session_state:
    st.session_state['db'] = []

st.title("🏥 MedGuard AI: Intelligent Triage")
st.markdown("---")

# --- 2. LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Patient Intake")
    raw_text = st.text_area("Paste Intake Form / Notes here:", height=250, 
                            placeholder="Example: PT-001, John Doe, chest pain, allergic to penicillin")
    
    if st.button("🔍 Screen Patient", type="primary"):
        if raw_text:
            # --- MOCK AI EXTRACTION ---
            # We use simple logic to 'pretend' the AI extracted the data
            text_low = raw_text.lower()
            
            # Identify Risk
            risk = "SAFE"
            icon = "🟢"
            if any(word in text_low for word in ["chest", "breath", "penicillin", "heart"]):
                risk = "CRITICAL"
                icon = "🔴"
            elif any(word in text_low for word in ["fever", "pain", "high"]):
                risk = "MODERATE"
                icon = "🟡"

            # Create Record
            new_record = {
                "name": "Patient Detected" if "pt" not in text_low else "PT-001 / John Doe",
                "risk": risk,
                "icon": icon,
                "note": raw_text[:50] + "...",
                "time": datetime.now().strftime("%H:%M:%S")
            }
            
            st.session_state['db'].append(new_record)
            st.success(f"Screening Complete: {risk}")
        else:
            st.error("Please enter patient notes.")

with col2:
    st.subheader("📊 Triage Dashboard")
    if not st.session_state['db']:
        st.info("Waiting for data...")
    else:
        for record in reversed(st.session_state['db']):
            # Color coding for Milestone 4
            color = "#ffcccc" if record['risk'] == "CRITICAL" else "#fff4cc" if record['risk'] == "MODERATE" else "#ccffcc"
            
            with st.container():
                st.markdown(f"""
                <div style="background-color:{color}; padding:15px; border-radius:10px; margin-bottom:10px; color:black; border-left: 8px solid #333;">
                    <strong>{record['icon']} {record['risk']}</strong> | {record['name']}<br>
                    <small>Received at: {record['time']}</small><br>
                    <p style="font-size: 12px;">{record['note']}</p>
                </div>
                """, unsafe_allow_stdio=True)
