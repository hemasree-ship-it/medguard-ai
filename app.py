import streamlit as st
import google.generativeai as genai
import json

# --- CONFIG ---
st.set_page_config(page_title="MedGuard AI", page_icon="🏥")
st.title("🏥 MedGuard AI Triage")

# Get API Key from Streamlit Secrets (We will set this in Step 3)
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
else:
    st.error("Please set the GEMINI_KEY in secrets!")

model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI ---
input_text = st.text_area("Paste Patient Intake Form:", height=200, placeholder="Example: PT-001, John Doe, chest pain, allergic to penicillin")

if st.button("Screen Patient"):
    if input_text:
        # 1. AI Extraction
        prompt = f"Extract to JSON with keys: name, symptoms, allergies. Text: {input_text}"
        response = model.generate_content(prompt)
        data = json.loads(response.text.replace("```json", "").replace("```", "").strip())
        
        # 2. Triage Logic
        risk = "SAFE 🟢"
        text_check = (str(data.get('symptoms')) + str(data.get('allergies'))).lower()
        if any(word in text_check for word in ["chest", "breath", "penicillin", "heart"]):
            risk = "CRITICAL 🔴"
        elif any(word in text_check for word in ["fever", "pain", "high"]):
            risk = "MODERATE 🟡"

        # 3. Show Results
        st.subheader(f"Status: {risk}")
        st.write(f"**Name:** {data.get('name')}")
        st.write(f"**Symptoms:** {data.get('symptoms')}")
        st.write(f"**Allergies:** {data.get('allergies')}")
    else:
        st.warning("Please enter text first.")
