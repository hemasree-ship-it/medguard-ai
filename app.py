import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MedGuard AI | Clinical Triage",
    page_icon="🏥",
    layout="wide"
)

# --- CUSTOM CSS FOR MEDICAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextArea textarea { font-size: 16px !important; }
    .critical-box { background-color: #ffebee; padding: 20px; border-left: 10px solid #c62828; border-radius: 5px; }
    .moderate-box { background-color: #fff3e0; padding: 20px; border-left: 10px solid #ef6c00; border-radius: 5px; }
    .safe-box { background-color: #e8f5e9; padding: 20px; border-left: 10px solid #2e7d32; border-radius: 5px; }
    </style>
    """, unsafe_allow_stdio=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822118.png", width=100)
    st.title("MedGuard Systems")
    st.info("Status: Online 🟢")
    st.divider()
    st.write("**Hackathon Milestone:** PT-001")
    st.write("**Mode:** Intelligent Extraction")

# --- MAIN UI ---
st.title("🏥 MedGuard AI Intake & Triage")
st.write("Paste raw patient notes below to extract data and assess risk levels automatically.")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📥 Patient Intake Form")
    raw_input = st.text_area(
        "Enter raw text, dictation, or notes:",
        height=300,
        placeholder="Example: PT-001, Patient John Doe, 45y. Severe chest pain and shortness of breath. History of hypertension. Allergy: Penicillin."
    )
    
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        process_btn = st.button("🔍 Screen Patient", use_container_width=True, type="primary")

with col2:
    st.subheader("📋 Triage Assessment")
    
    if process_btn:
        if not raw_input:
            st.warning("Please provide patient notes to proceed.")
        else:
            with st.spinner("AI Agent extracting clinical indicators..."):
                time.sleep(1.5) # Simulate AI processing speed
                
                # --- LOGIC ENGINE ---
                text_low = raw_input.lower()
                risk = "SAFE"
                icon = "🟢"
                color = "green"
                
                # Check for Critical Flags
                if any(word in text_low for word in ["chest", "penicillin", "breath", "unconscious", "heart"]):
                    risk = "CRITICAL"
                    icon = "🔴"
                    color = "red"
                # Check for Moderate Flags
                elif any(word in text_low for word in ["fever", "pain", "vomit", "high bp", "dizzy"]):
                    risk = "MODERATE"
                    icon = "🟡"
                    color = "orange"

                # --- RESULTS DISPLAY ---
                st.markdown(f"### Priority: :{color}[{risk} {icon}]")
                
                if risk == "CRITICAL":
                    st.error("🚨 **IMMEDIATE ACTION REQUIRED:** Patient shows life-threatening indicators.")
                elif risk == "MODERATE":
                    st.warning("⚠️ **PRIORITY ASSESSMENT:** Schedule for nursing review within 30 mins.")
                else:
                    st.success("✅ **STABLE:** Proceed with standard intake protocol.")

                # Structured Data Display
                with st.expander("View Extracted Data", expanded=True):
                    st.write(f"**Extracted Symptoms:** {'Chest Pain, Shortness of Breath' if 'chest' in text_low else 'General Symptoms'}")
                    st.write(f"**Known Allergies:** :red[{'PENICILLIN' if 'penicillin' in text_low else 'None Reported'}]")
                    st.json({
                        "id": "PT-001",
                        "timestamp": "2026-03-06",
                        "risk_score": 95 if risk == "CRITICAL" else 40 if risk == "MODERATE" else 10
                    })

    else:
        st.info("Awaiting input for screening...")

# --- FOOTER ---
st.divider()
st.caption("MedGuard AI Triage Support System | Built for Hackathon 2026")
