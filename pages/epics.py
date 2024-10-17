import streamlit as st
from ELSA.assistant_handlers import handle_predefined_questions, handle_user_queries
from ELSA.session_utils import init_session_state, init_assistant_client
from ELSA.auth import authenticate


def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main():
    authenticate()

    # If the user is authenticated, show the main app content
    if st.session_state.authentication_status:
        init_session_state()
        init_assistant_client()
        display_chat_messages()
        
        # Handle predefined questions or chat input based on interaction state
        if not st.session_state.assistant_started:
            handle_predefined_questions()
        else:
            handle_user_queries()
