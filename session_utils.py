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
        "predefined_responses": [],  # Store user responses to predefined questions
        "assistant_started": False,  # Flag to track if assistant interaction started
        "thread_id": None,
        "assistant_client": None,  # Store the assistant client object
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# def init_session_state():
#     if "openai_model" not in st.session_state:
#         st.session_state.openai_model = "gpt-4o-2024-08-06"
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "current_question_index" not in st.session_state:
#         st.session_state.current_question_index = 0
#     if "predefined_responses" not in st.session_state:
#         st.session_state.predefined_responses = []  # Store user responses to predefined questions
#     if "assistant_started" not in st.session_state:
#         st.session_state.assistant_started = False  # Flag to track if assistant interaction started
#     if "thread_id" not in st.session_state:
#             st.session_state.thread_id = None


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