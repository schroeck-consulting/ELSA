import streamlit as st
from assistant_handlers import handle_predefined_questions, handle_user_queries
from session_utils import init_session_state, init_assistant_client


PREDEFINED_QUESTIONS = [
    "1.	What Team will be implementing this requirement?",
    "2.	I see that (BAT) often works also with the following teams. Are any of them also involved for this epic?",
    "3.	Brief description of what you want",
    "4. How is this different from what we are already doing?",
    "5. Which of your stakeholders will benefit from this epic? + benefits",
    "6. You usually work with the following technical components. Which components are likely to be impacted?",
    "7. Do you need new input data for this epic?\n IF yes, what new data and from which system is it needed?",
    "8. Are you providing new output data?\n IF yes, what new data are you outputting and where is it being sent to?",
    "9.	Do you have any reference (similar) epics that can help me better understand your requirement?",
    "10. Are there any sections in the questionnaire that require further input on clarity?",
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
