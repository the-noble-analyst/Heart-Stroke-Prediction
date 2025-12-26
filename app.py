import streamlit as st
from ui import render_ui
from model_loader import load_models
from together_client import get_together_client
from state import init_state

model, scaler, expected_columns = load_models()
client = get_together_client()
init_state()

render_ui(model, scaler, expected_columns, client)
