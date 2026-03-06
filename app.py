import streamlit as st
import time

# 1. Page Setup
st.set_page_config(page_title="MedGuard AI", page_icon="🏥")

# 2. Sidebar
st.sidebar.title("🏥 MedGuard System")
st.sidebar.info("Status: Operational")

# 3. Main UI
st.title("MedGuard AI Triage")
st.write("Enter patient notes below to screen for risks.")

# Input Box
raw_input = st.text_area("Patient Intake Text:", height=200)

if st.button("Screen Patient"):
    if raw_input:
        with st.spinner("Analyzing..."):
            time.sleep(1) # Fake delay
            
            # Logic
            text_low = raw_input.lower()
            risk = "SAFE"
            
            if any(word in text_low for word in ["chest", "penicillin", "breath", "heart"]):
                risk = "CRITICAL"
            elif any(word in text_low for word in ["fever", "pain", "high"]):
                risk = "MODERATE"
            
            # Results
            st.divider()
            if risk == "CRITICAL":
                st.error(f"### TRIAGE LEVEL: {risk} 🔴")
                st.write("**Action:** Immediate Doctor Notification.")
            elif risk == "MODERATE":
                st.warning(f"### TRIAGE LEVEL: {risk} 🟡")
                st.write("**Action:** Priority Nursing Intake.")
            else:
                st.success(f"### TRIAGE LEVEL: {risk} 🟢")
                st.write("**Action:** Standard Procedure.")

            # Data Summary
            st.subheader("Extracted Details")
            st.write(f"**Primary Flag:** {'Allergy/Cardiac' if risk == 'CRITICAL' else 'General'}")
            st.json({"id": "PT-001", "risk_level": risk})
    else:
        st.warning("Please enter text.")
