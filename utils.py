import time
import streamlit as st

def display_typing_effect(text: str):
    """Simulates typing effect in Streamlit."""
    placeholder = st.empty()
    full_text = ""
    for char in text:
        full_text += char
        placeholder.markdown(full_text)
        time.sleep(0.002)  # Adjust the speed as needed
