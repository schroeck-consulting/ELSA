import streamlit as st
import os
from dotenv import load_dotenv
from assistant_api import AssistantClient
from copy import deepcopy


GREATING_MESSAGE = "Welcome! I'm ELSA, here to assist you in creating detailed and well-structured epics.\nI will ask you some questions to get into the context and guide you through the process.\nLet's get started!"

PREDEFINED_QUESTIONS = [
    {"id": "team", "question": "**What Team will be implementing this requirement?**"},
    {"id": "teams_involved", "question": "**Are any other teams also involved in this epic?**"},
    {"id": "summary", "question": "**Please provide a brief description of what you'd like to achieve**"},
    {"id": "differences", "question": "**How is it different to what we are already doing?**"},
    {"id": "stakeholders", "question": "**Which of your stakeholders benefit from this epic?**"},
    {"id": "technical_components", "question": "**Which technical components do you think are likely to be impacted?**"},
    {"id": "input_data", "question": "**Do you need new input data for this epic?**"},
    {"id": "output_data", "question": "**Are you providing new output data?**"},
    ]


def init_session_state():
    """
    Initializes session state variables used throughout the app.
    """
    defaults = {
        "openai_model": "gpt-4o-2024-08-06",
        "assistant_client": None,

        "messages": [{"role": "assistant", "content": GREATING_MESSAGE}],
        "assistant_started": False,
        "chat_started": False,
        # "modified_epic": "",
                
        "team_name": None,
        "stakeholders": [],
        "input_data": None,
        "output_data": None,
        
        "question_to_suggestions": {},
        "questions_to_ask": PREDEFINED_QUESTIONS,
        "questions_asked": [],
        "user_responses": [],
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(value)
            

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
