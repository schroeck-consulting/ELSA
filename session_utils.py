import streamlit as st
import os
from dotenv import load_dotenv
from assistant_api import AssistantClient

def init_session_state():
    """
    Initializes session state variables used throughout the app.
    """
    defaults = {
        "openai_model": "gpt-4o-2024-08-06",
        "messages": [],
        "current_question_index": 0,
        "predefined_responses": [],
        "assistant_started": False,
        "thread_id": None,
        "assistant_client": None,
        "team_name": None,
        "stakeholders": None,
        "question_to_suggestions": {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            

def init_assistant_client():
    """
    Initializes the OpenAI Assistant Client and creates a thread.
    """
    if not st.session_state.assistant_client:
        load_dotenv()
        assistant_id = os.getenv("ASSISTANT_ID")
        api_key = os.getenv("OPENAI_API_KEY")
        st.session_state.assistant_client = AssistantClient(api_key=api_key, assistant_id=assistant_id)

        # Create a new thread for the conversation if it doesn't exist
        thread = st.session_state.assistant_client.create_thread()
        st.session_state.thread_id = thread.id