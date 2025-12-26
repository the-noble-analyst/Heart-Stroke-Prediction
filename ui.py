import streamlit as st
import pandas as pd
from datetime import datetime
from pdf_report import generate_pdf_report


def render_ui(model, scaler, expected_columns, client):

    # -------------------------
    # Page Config
    # -------------------------
    st.set_page_config(
        page_title="HeartAlert - AI Heart Health Assistant",
        page_icon="❤️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # -------------------------
    # Global Styles
    # -------------------------
    st.markdown("""
    <style>
        * { font-family: 'Inter', sans-serif; }
        .block-container { max-width: 1200px; padding-top: 1.5rem; }
        h1, h2, h3 { color: #1f2937; }
        .card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .soft-card {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.5rem;
        }
        .metric {
            font-size: 1.8rem;
            font-weight: 600;
            color: #3b82f6;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #6b7280;
        }
        .primary-btn button {
            background: #3b82f6;
            border-radius: 10px;
            font-weight: 500;
            padding: 0.7rem;
        }
        #MainMenu, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------
    # Header
    # -------------------------
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        try:
            st.image("HeartProjectLogo.png", width=240)
        except:
            st.markdown("<h1 style='text-align:center;'>❤️ HeartAlert</h1>", unsafe_allow_html=True)

    # -------------------------
    # Hero Section
    # -------------------------
    st.markdown("""
    <div class="card" style="text-align:center;">
        <h2>AI-Powered Heart Disease Risk Assessment</h2>
        <p style="color:#6b7280; max-width:700px; margin:auto;">
        Get instant insights into your heart health using machine learning.
        Analyze vital signs, assess risk, and receive personalized guidance.
        </p>
        <div style="display:flex; justify-content:center; gap:3rem; margin-top:1.5rem; flex-wrap:wrap;">
            <div>
                <div class="metric">88.6%</div>
                <div class="metric-label">Model Accuracy</div>
            </div>
            <div>
                <div class="metric">&lt; 30s</div>
                <div class="metric-label">Analysis Time</div>
            </div>
            <div>
                <div class="metric">24/7</div>
                <div class="metric-label">AI Support</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # AI Chat Section
    # -------------------------
    st.markdown("### 💬 AI Health Assistant")
    st.markdown("Ask questions about heart health, symptoms, or this assessment.")

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "❤️"):
                st.markdown(msg["content"])

    if user_input := st.chat_input("Ask me anything about heart health..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})

        try:
            messages = [
                {"role": "system", "content": "You are HeartAlert, a professional and caring heart health AI assistant."}
            ] + st.session_state["messages"]

            response = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            reply = response.choices[0].message.content.strip()
            reply = reply.replace("**", "").replace("*", "")
            st.session_state["messages"].append({"role": "assistant", "content": reply})
            st.rerun()

        except Exception as e:
            st.error(f"Chat error: {e}")

    st.markdown("---")

    # -------------------------
    # Assessment Form
    # -------------------------
    st.markdown("### 🩺 Patient Assessment")

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Personal Information**")
            name = st.text_input("Full Name *")
            age = st.slider("Age", 18, 100, 40)
            sex = st.selectbox("Gender", ["M", "F"], format_func=lambda x: "Male" if x == "M" else "Female")

        with col2:
            st.markdown("**Symptoms & Concerns**")
            symptoms = st.text_area(
                "Describe your symptoms *",
                height=120,
                placeholder="Chest pain, breathlessness, fatigue, dizziness..."
            )

    st.markdown("**Vital Signs & Medical Information**")

    col3, col4, col5 = st.columns(3)

    with col3:
        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
        max_hr = st.slider("Maximum Heart Rate", 60, 220, 150)
        chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])

    with col4:
        cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
        oldpeak = st.slider("Oldpeak", 0.0, 6.0, 1.0, 0.1)
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])

    with col5:
        resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
        exercise_angina = st.selectbox("Exercise-Induced Angina", ["N", "Y"])
        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    st.markdown("---")

    # -------------------------
    # Analyze
    # -------------------------
    analyze = st.button("Analyze Heart Health", use_container_width=True)

    if analyze:
        if not name or not symptoms:
            st.error("Please enter your name and symptoms.")
            return

        raw_input = {
            'Age': age,
            'RestingBP': resting_bp,
            'Cholesterol': cholesterol,
            'FastingBS': fasting_bs,
            'MaxHR': max_hr,
            'Oldpeak': oldpeak,
            'Gender_' + sex: 1,
            'ChestPainType_' + chest_pain: 1,
            'RestingECG_' + resting_ecg: 1,
            'ExerciseAngina_' + exercise_angina: 1,
            'ST_Slope_' + st_slope: 1
        }

        df = pd.DataFrame([raw_input])
        for col in expected_columns:
            if col not in df:
                df[col] = 0
        df = df[expected_columns]

        scaled = scaler.transform(df)
        prediction = model.predict(scaled)[0]

        st.session_state["prediction"] = prediction
        st.session_state["prediction_made"] = True
        st.session_state["user_data"] = {
            "name": name,
            "Age": age,
            "sex": "Male" if sex == "M" else "Female",
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "MaxHR": max_hr,
            "chest_pain": chest_pain,
            "oldpeak": oldpeak,
            "fasting_bs": fasting_bs,
            "resting_ecg": resting_ecg,
            "exercise_angina": "Yes" if exercise_angina == "Y" else "No",
            "st_slope": st_slope,
            "symptoms": symptoms
        }

        if prediction == 1:
            st.error("HIGH RISK of Heart Disease Detected")
        else:
            st.success("LOW RISK of Heart Disease")

    # -------------------------
    # PDF Download
    # -------------------------
    if st.session_state.get("prediction_made"):
        if st.button("Download Complete Report (PDF)", use_container_width=True):
            pdf_bytes = generate_pdf_report(
                st.session_state["user_data"],
                st.session_state["prediction"],
                st.session_state.get("tips", ""),
                st.session_state["user_data"]["symptoms"],
                st.session_state["messages"]
            )

            st.download_button(
                "Download PDF",
                pdf_bytes,
                file_name=f"HeartAlert_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
