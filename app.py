import os
from together import Together
import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from fpdf import FPDF

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
# Custom CSS for Professional UI
# -------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-in-out;
    }
    
    .logo-container img {
        max-width: 350px;
        filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));
        animation: pulse 2s infinite;
    }
    
    /* AI Chat Button */
    .ai-chat-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        animation: bounce 2s infinite;
    }
    
    .ai-chat-button button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        font-size: 2rem;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .ai-chat-button button:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(239, 68, 68, 0.7);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Card styling */
    .stApp > div > div {
        background: white;
        border-radius: 25px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        animation: slideInLeft 0.8s ease-out;
    }
    
    /* Section headers */
    .section-header {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        padding-left: 15px;
        border-left: 5px solid #667eea;
        animation: slideInLeft 0.6s ease-out;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #f9fafb;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Labels */
    label {
        font-weight: 600;
        color: #374151;
        font-size: 0.95rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1.2rem 2.5rem;
        font-size: 1.2rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
    }
    
    /* Chat messages */
    .stChatMessage {
        border-radius: 15px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Success/Error boxes */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    }
    
    .stError, .stWarning {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
    }
    
    /* Quick question buttons */
    .quick-question {
        background: white;
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        color: #667eea;
        font-weight: 600;
    }
    
    .quick-question:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Load Model & Preprocessing
# -------------------------
@st.cache_resource
def load_models():
    model = joblib.load("KNN_heart.pkl")
    scaler = joblib.load("scaler.pkl")
    expected_columns = joblib.load("columns.pkl")
    return model, scaler, expected_columns

model, scaler, expected_columns = load_models()

# -------------------------
# Setup Together Client
# -------------------------
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=TOGETHER_API_KEY)

# -------------------------
# PDF Report Generation
# -------------------------
class HeartAlertReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 24)
        self.set_text_color(102, 126, 234)
        self.cell(0, 12, 'HeartAlert', 0, 1, 'C')
        self.set_font('Arial', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'AI-Powered Heart Health Assessment Report', 0, 1, 'C')
        self.ln(8)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Generated by HeartAlert - Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(102, 126, 234)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, body)
        self.ln()

def generate_pdf_report(user_data, prediction, tips, symptoms, chat_history):
    pdf = HeartAlertReport()
    pdf.add_page()
    
    # Patient Information
    pdf.chapter_title('PATIENT INFORMATION')
    patient_info = f"""Name: {user_data['name']}
Date: {datetime.now().strftime('%B %d, %Y')}
Time: {datetime.now().strftime('%I:%M %p')}
Report ID: HRT-{datetime.now().strftime('%Y%m%d%H%M%S')}"""
    pdf.chapter_body(patient_info)
    
    # Symptoms
    if symptoms:
        pdf.chapter_title('REPORTED SYMPTOMS')
        pdf.chapter_body(symptoms)
    
    # Health Metrics
    pdf.chapter_title('HEALTH METRICS')
    metrics = f"""Age: {user_data['Age']} years
Gender: {user_data['sex']}
Resting Blood Pressure: {user_data['RestingBP']} mm Hg
Cholesterol: {user_data['Cholesterol']} mg/dL
Maximum Heart Rate: {user_data['MaxHR']} bpm
Chest Pain Type: {user_data['chest_pain']}
Oldpeak (ST Depression): {user_data['oldpeak']}
Fasting Blood Sugar: {'> 120 mg/dL' if user_data['fasting_bs'] else '< 120 mg/dL'}
Resting ECG: {user_data['resting_ecg']}
Exercise Angina: {user_data['exercise_angina']}
ST Slope: {user_data['st_slope']}"""
    pdf.chapter_body(metrics)
    
    # Assessment Result
    pdf.chapter_title('RISK ASSESSMENT')
    pdf.set_font('Arial', 'B', 12)
    if prediction == 1:
        pdf.set_text_color(220, 38, 38)
        result = "HIGH RISK - Immediate medical consultation recommended"
    else:
        pdf.set_text_color(34, 197, 94)
        result = "LOW RISK - Continue maintaining healthy lifestyle"
    pdf.multi_cell(0, 8, result)
    pdf.set_text_color(0, 0, 0)
    pdf.ln()
    
    # AI Recommendations
    pdf.chapter_title('PERSONALIZED HEALTH RECOMMENDATIONS')
    pdf.chapter_body(tips)
    
    # Chat History
    if len(chat_history) > 0:
        pdf.add_page()
        pdf.chapter_title('AI CONSULTATION CONVERSATION')
        for msg in chat_history:
            if msg['role'] == 'user':
                pdf.set_font('Arial', 'B', 10)
                pdf.set_text_color(102, 126, 234)
                pdf.multi_cell(0, 6, f"Patient: {msg['content']}")
                pdf.ln(2)
            elif msg['role'] == 'assistant':
                pdf.set_font('Arial', '', 10)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(0, 6, f"HeartAlert AI: {msg['content']}")
                pdf.ln(3)
    
    # Disclaimer
    pdf.add_page()
    pdf.chapter_title('MEDICAL DISCLAIMER')
    disclaimer = """This report is generated by HeartAlert, an AI-powered heart health assessment tool. This is NOT a substitute for professional medical advice, diagnosis, or treatment.

Always seek the advice of your physician or other qualified health provider with any questions regarding a medical condition. Never disregard professional medical advice or delay seeking it because of information from this report.

HeartAlert uses machine learning algorithms to provide risk assessment based on the data provided. Results should be discussed with a healthcare professional for proper interpretation and action.

This report is for informational purposes only and should be presented to a licensed medical professional for validation and further evaluation.

HeartAlert is a verified AI health assessment platform designed to assist healthcare professionals and patients in preliminary risk screening."""
    pdf.chapter_body(disclaimer)
    
    # Footer certification
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(102, 126, 234)
    pdf.cell(0, 6, 'Verified AI Health Assessment Platform', 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin1')

# -------------------------
# Initialize Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "prediction_made" not in st.session_state:
    st.session_state["prediction_made"] = False

if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

if "show_chat_modal" not in st.session_state:
    st.session_state["show_chat_modal"] = False

# -------------------------
# Header with Logo
# -------------------------
try:
    st.image("logo.png", use_column_width=False, width=350)
except:
    st.markdown('<h1 style="text-align: center; color: white; font-size: 3.5rem; font-weight: 800; margin: 1rem 0; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);">❤️ HeartAlert</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #e0e7ff; font-size: 1.3rem; margin-bottom: 2rem;">Your AI-Powered Heart Health Companion</p>', unsafe_allow_html=True)

# -------------------------
# AI Chat Button (Floating)
# -------------------------
col_float1, col_float2 = st.columns([5, 1])
with col_float2:
    if st.button("❤️\n💬", key="ai_chat_float", help="Ask AI"):
        st.session_state["show_chat_modal"] = not st.session_state["show_chat_modal"]

# -------------------------
# AI Chat Modal
# -------------------------
if st.session_state["show_chat_modal"]:
    st.markdown("---")
    st.markdown('<p class="section-header">💬 AI Health Assistant</p>', unsafe_allow_html=True)
    
    # Quick Questions
    st.markdown("### 🔥 Quick Questions")
    
    quick_questions = [
        "What are the warning signs of a heart attack?",
        "How can I lower my cholesterol naturally?",
        "What does high blood pressure mean?",
        "How does this AI prediction work?",
        "What lifestyle changes can improve heart health?",
        "What do my test results mean?",
        "When should I see a cardiologist?",
        "How can I prevent heart disease?"
    ]
    
    cols = st.columns(2)
    for idx, question in enumerate(quick_questions):
        with cols[idx % 2]:
            if st.button(f"❓ {question}", key=f"quick_q_{idx}", use_container_width=True):
                st.session_state["messages"].append({"role": "user", "content": question})
                st.rerun()
    
    st.markdown("---")
    
    # Display chat messages
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="❤️"):
                st.markdown(msg["content"])
    
    # Chat input
    if user_input := st.chat_input("Ask me anything about heart health..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        with st.chat_message("assistant", avatar="❤️"):
            with st.spinner("Thinking..."):
                try:
                    system_message = """You are HeartAlert, a professional and caring heart health AI assistant. 
                    Provide evidence-based, supportive, and actionable health guidance. 
                    Be empathetic but clear. Keep responses concise and well-formatted.
                    If the user asks about specific symptoms or medical advice, 
                    always remind them to consult a healthcare professional."""
                    
                    messages = [{"role": "system", "content": system_message}] + st.session_state["messages"]
                    
                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=500
                    )
                    ai_reply = response.choices[0].message.content.strip()
                    st.session_state["messages"].append({"role": "assistant", "content": ai_reply})
                    st.markdown(ai_reply)
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Chat error: {e}")
    
    # Close button
    if st.button("✖️ Close Chat", use_container_width=True):
        st.session_state["show_chat_modal"] = False
        st.rerun()
    
    st.markdown("---")

# -------------------------
# Main Assessment Form
# -------------------------
st.markdown('<p class="section-header">📋 Patient Assessment Form</p>', unsafe_allow_html=True)

# Personal Information
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 👤 Personal Information")
    user_name = st.text_input("Full Name *", placeholder="Enter your full name")
    age = st.slider("Age", 18, 100, 40)
    sex = st.selectbox("Gender", ["M", "F"], format_func=lambda x: "Male" if x == "M" else "Female")

with col2:
    st.markdown("#### 🩺 Symptoms & Concerns")
    symptoms = st.text_area(
        "Describe any symptoms you're experiencing *",
        placeholder="E.g., chest pain, shortness of breath, fatigue, dizziness, palpitations...",
        height=120
    )

st.markdown("---")

# Vital Signs
st.markdown("#### 📊 Vital Signs & Medical Information")

col3, col4, col5 = st.columns(3)

with col3:
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
    max_hr = st.slider("Maximum Heart Rate (bpm)", 60, 220, 150)
    chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"],
                             help="ATA: Atypical Angina, NAP: Non-Anginal Pain, TA: Typical Angina, ASY: Asymptomatic")

with col4:
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
    oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0, 0.1)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1],
                             format_func=lambda x: "No" if x == 0 else "Yes")

with col5:
    resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"],
                              help="Normal, ST: ST-T wave abnormality, LVH: Left Ventricular Hypertrophy")
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["N", "Y"],
                                  format_func=lambda x: "No" if x == "N" else "Yes")
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"],
                           help="Slope of peak exercise ST segment")

st.markdown("---")

# -------------------------
# Analyze Button
# -------------------------
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    analyze_btn = st.button("🔍 Analyze Heart Health", use_container_width=True)

if analyze_btn:
    if not user_name or not symptoms:
        st.error("⚠️ Please enter your full name and describe your symptoms before proceeding.")
    else:
        with st.spinner("🔄 Analyzing your heart health data..."):
            # Prepare input
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

            input_df = pd.DataFrame([raw_input])

            # Fill missing columns
            for col in expected_columns:
                if col not in input_df.columns:
                    input_df[col] = 0

            # Reorder columns
            input_df = input_df[expected_columns]

            # Scale input
            scaled_input = scaler.transform(input_df)

            # Predict
            prediction = model.predict(scaled_input)[0]
            
            # Store data for report
            st.session_state["user_data"] = {
                'name': user_name,
                'Age': age,
                'sex': 'Male' if sex == 'M' else 'Female',
                'RestingBP': resting_bp,
                'Cholesterol': cholesterol,
                'MaxHR': max_hr,
                'chest_pain': chest_pain,
                'oldpeak': oldpeak,
                'fasting_bs': fasting_bs,
                'resting_ecg': resting_ecg,
                'exercise_angina': 'Yes' if exercise_angina == 'Y' else 'No',
                'st_slope': st_slope,
                'symptoms': symptoms
            }
            st.session_state["prediction"] = prediction
            st.session_state["prediction_made"] = True

            # Display prediction
            st.markdown("---")
            if prediction == 1:
                st.error("### ⚠️ HIGH RISK of Heart Disease Detected")
                st.warning("""
                **Immediate Action Recommended:**
                - Consult a cardiologist as soon as possible
                - Do not ignore this assessment
                - Download your report and bring it to your doctor
                """)
            else:
                st.success("### ✅ LOW RISK of Heart Disease")
                st.info("""
                **Great News!** Your current health metrics indicate a lower risk. 
                Continue maintaining a healthy lifestyle and regular check-ups.
                """)

            # Generate AI Recommendations
            st.markdown("---")
            st.markdown('<p class="section-header">💡 Personalized Health Recommendations</p>', unsafe_allow_html=True)
            
            with st.spinner("🤖 Generating personalized health tips..."):
                prompt = f"""
                Patient Information:
                - Name: {user_name}
                - Age: {age}, Gender: {'Male' if sex == 'M' else 'Female'}
                - Blood Pressure: {resting_bp} mm Hg
                - Cholesterol: {cholesterol} mg/dL
                - Max Heart Rate: {max_hr} bpm
                - Symptoms: {symptoms}
                - Risk Assessment: {'HIGH RISK' if prediction == 1 else 'LOW RISK'}

                Provide 4-5 specific, actionable health recommendations in clear sections:
                1. Immediate Actions (if high risk) or Preventive Measures (if low risk)
                2. Dietary Recommendations
                3. Exercise Guidelines
                4. Lifestyle Modifications
                5. Medical Follow-up

                Be empathetic, encouraging, and professional. Use simple headings without asterisks.
                """

                try:
                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                        messages=[
                            {"role": "system", "content": "You are HeartAlert AI. Provide clear, well-structured health recommendations. Use simple numbered sections without markdown symbols."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=700
                    )
                    tips = response.choices[0].message.content.strip()
                    # Remove all markdown symbols
                    tips_clean = tips.replace('**', '').replace('*', '').replace('#', '')
                    st.session_state["tips"] = tips_clean

                    st.markdown(f"""
                    <div class="info-box">
                    {tips_clean}
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error generating recommendations: {e}")
                    st.session_state["tips"] = "Unable to generate recommendations at this time."

# -------------------------
# Download Report
# -------------------------
if st.session_state["prediction_made"]:
    st.markdown("---")
    col_report1, col_report2, col_report3 = st.columns([1, 2, 1])
    
    with col_report2:
        if st.button("📄 Download Complete Report (PDF)", use_container_width=True):
            with st.spinner("📝 Generating your comprehensive health report..."):
                try:
                    pdf_bytes = generate_pdf_report(
                        st.session_state["user_data"],
                        st.session_state["prediction"],
                        st.session_state.get("tips", ""),
                        st.session_state["user_data"]["symptoms"],
                        st.session_state["messages"]
                    )
                    
                    st.download_button(
                        label="⬇️ Click Here to Download Your Report",
                        data=pdf_bytes,
                        file_name=f"HeartAlert_Report_{st.session_state['user_data']['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ Report generated successfully! This includes your assessment, AI recommendations, and complete chat history.")
                    
                except Exception as e:
                    st.error(f"Error generating report: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;'>
    <p><strong>HeartAlert</strong> - AI-Powered Heart Health Assistant</p>
    <p style='font-size: 0.9rem;'>This tool is for informational purposes only and is not a substitute for professional medical advice.</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>© 2024 HeartAlert. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
