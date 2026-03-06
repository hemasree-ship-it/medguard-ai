import streamlit as st
from datetime import datetime
import time

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(page_title="MedGuard AI | Clinical Triage", page_icon="🏥", layout="wide")

# Custom CSS for a Professional Hospital Theme
st.markdown("""
    <style>
    .main { background-color: #F0F2F6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004A99; color: white; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #004A99; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #004A99; }
    .triage-card {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 12px solid;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Session State for Database
if 'records' not in st.session_state:
    st.session_state['records'] = []

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3306/3306567.png", width=80)
    st.title("MedGuard Portal")
    st.write("Logged in as: **Triage Nurse (Station 1)**")
    st.divider()
    st.info("System Status: **Secure & Active**")
    if st.button("Clear Dashboard Cache"):
        st.session_state['records'] = []
        st.rerun()

# --- 3. MAIN INTERFACE ---
st.title("🏥 Clinical Intake & Triage Engine")
st.caption("City General Hospital | MedGuard AI v1.0")

col_input, col_dash = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Patient Submission")
    with st.container():
        raw_text = st.text_area(
            "Paste unstructured notes or dictated text here:", 
            height=300, 
            placeholder="Example: PT-001, Patient John Doe. Complaining of severe chest pain. Known allergy to penicillin."
        )
        
        if st.button("Analyze & Classify Patient"):
            if raw_text:
                with st.spinner("Processing clinical indicators..."):
                    time.sleep(1.2) # Simulated processing
                    
                    # --- TRIAGE LOGIC ENGINE ---
                    text_low = raw_text.lower()
                    if any(w in text_low for w in ["chest", "breath", "penicillin", "heart", "stroke"]):
                        risk, color, border = "CRITICAL", "#FFEBEE", "#D32F2F"
                    elif any(w in text_low for w in ["fever", "pain", "high bp", "vomit"]):
                        risk, color, border = "MODERATE", "#FFF3E0", "#F57C00"
                    else:
                        risk, color, border = "SAFE", "#E8F5E9", "#388E3C"

                    # Save Record
                    st.session_state['records'].append({
                        "id": f"CGH-{len(st.session_state['records'])+101}",
                        "risk": risk,
                        "color": color,
                        "border": border,
                        "body": raw_text[:100] + "...",
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    st.toast(f"Patient Classified as {risk}", icon="✅")
            else:
                st.error("Text field cannot be empty.")

with col_dash:
    st.subheader("📋 Priority Triage Queue")
    
    if not st.session_state['records']:
        st.write("---")
        st.info("No pending patients in queue.")
    else:
        # Metrics for trust
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(st.session_state['records']))
        c2.metric("Critical", len([r for r in st.session_state['records'] if r['risk'] == "CRITICAL"]))
        c3.metric("Avg Wait", "2m")
        
        st.write("---")
        
        # Display professional cards
        for r in reversed(st.session_state['records']):
            st.markdown(f"""
                <div class="triage-card" style="border-left-color: {r['border']};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: {r['border']}; font-weight: bold; font-size: 1.2em;">{r['risk']}</span>
                        <span style="color: grey;">ID: {r['id']}</span>
                    </div>
                    <p style="margin: 10px 0; color: #333;">{r['body']}</p>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8em; color: grey;">
                        <span>Recieved: {r['time']}</span>
                        <span><b>Status: Pending Review</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
