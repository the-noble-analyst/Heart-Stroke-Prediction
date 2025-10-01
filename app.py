import os
from together import Together
import streamlit as st
import pandas as pd
import joblib

# -------------------------
# Page Config (must be first Streamlit call)
# -------------------------
st.set_page_config(page_title="Heart Health Chatbot", page_icon="❤️", layout="centered")

# -------------------------
# Load Model & Preprocessing
# -------------------------
model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")

# -------------------------
# Setup Together Client
# -------------------------
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")  # Make sure to export API key
client = Together(api_key=TOGETHER_API_KEY)

# -------------------------
# Streamlit UI
# -------------------------
st.title("Heart Health Assistant")
st.markdown("Provide the following details to check your heart stroke risk:")

# Collect user input
age = st.slider("Age", 18, 100, 40)
sex = st.selectbox("Gender", ["M", "F"])
chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])
resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_hr = st.slider("Max Heart Rate", 60, 220, 150)
exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

# -------------------------
# Predict Button
# -------------------------
if st.button("Predict"):
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

    # Display prediction
    if prediction == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    # -------------------------
    # AI Health Tips
    # -------------------------
    prompt = f"""
    The user provided the following health details today: {raw_input}.
    The predicted heart stroke risk is {prediction} (1 = High Risk, 0 = Low Risk).

    Suggest 3–4 personalized, practical, and motivational health tips to:
    - Lower heart stroke risk
    - Improve heart health through lifestyle changes
    - Encourage positive habits (diet, exercise, stress management)
    - Highlight any medical checkups or precautions needed

    Keep the tone friendly, supportive, and easy to understand.
    Avoid medical jargon or sounding alarming — focus on encouragement and prevention.
    """

    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "You are a caring heart health assistant. Give short, actionable, and friendly health tips."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        tips = response.choices[0].message.content.strip()

        st.markdown("### 💡 Heart Health Suggestions:")
        st.markdown(tips)

        # Save AI suggestions in chat history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "system", "content": "You are a caring heart health assistant."}]
        st.session_state["messages"].append({"role": "assistant", "content": tips})

    except Exception as e:
        st.error(f"Error generating tips: {e}")


# =========================
# 🔹 Chat Interface
# =========================
st.markdown("## 💬 Continue Chatting with Your AI Coach")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a caring heart health assistant."}]

# Display past messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything about heart health..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=st.session_state["messages"],
            temperature=0.7,
            max_tokens=500
        )
        ai_reply = response.choices[0].message.content.strip()
        st.session_state["messages"].append({"role": "assistant", "content": ai_reply})
        st.chat_message("assistant").markdown(ai_reply)
    except Exception as e:
        st.error(f"⚠️ Chat error: {e}")

    except Exception as e:
        st.error(f"Error generating tips with Together.ai: {e}")
