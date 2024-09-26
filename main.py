import streamlit as st
from assistant_handlers import handle_predefined_questions, handle_user_queries
from session_utils import init_session_state, init_assistant_client


def main():
    st.title("Epic Builder Copilot")

    init_session_state()
    init_assistant_client()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle predefined questions or chat input based on interaction state
    if not st.session_state.assistant_started:
        handle_predefined_questions()
    else:
        handle_user_queries()

if __name__ == "__main__":
    main()
