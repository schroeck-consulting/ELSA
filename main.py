import streamlit as st
from assistant_handlers import handle_predefined_questions, handle_user_queries
from session_utils import init_session_state, init_assistant_client


PREDEFINED_QUESTIONS = [
    {"id": "team", "question": "1. What Team will be implementing this requirement?"},
    {"id": "teams_involved", "question": "2. I see that {team} often works also with the following teams. Are any of them also involved for this epic?"},
    {"id": "summary", "question": "3. Brief description of what you want"},
    {"id": "differences", "question": "4. How is it different to what we are already doing?"},
    {"id": "stakeholders", "question": "5. Which of your stakeholders benefit from this epic? "},
    {"id": "technical_components", "question": "6. I think you usually work with the following technical components. Which technical components do you think are likely to be impacted? "},
    {"id": "input_data", "question": "7. Do you need new input data for this epic?"},
    {"id": "output_data", "question": "8. Are you providing new output data?"},
    # {"id": "", "question": ""},
    ]

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
        handle_predefined_questions(PREDEFINED_QUESTIONS)
    else:
        handle_user_queries()

if __name__ == "__main__":
    main()
