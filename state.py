import streamlit as st

def init_state():
    defaults = {
        "messages": [],
        "prediction_made": False,
        "user_data": {},
        "show_chat_modal": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
