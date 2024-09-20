import streamlit as st
import os
import time
from dotenv import load_dotenv
from assistant_api import AssistantClient
from utils import display_typing_effect


def init_session_state():
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o-2024-08-06"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "predefined_responses" not in st.session_state:
        st.session_state.predefined_responses = []  # Store user responses to predefined questions
    if "assistant_started" not in st.session_state:
        st.session_state.assistant_started = False  # Flag to track if assistant interaction started
    if "thread_id" not in st.session_state:
            st.session_state.thread_id = None

predefined_questions = [
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

    # Initialize OpenAI Assistant Client
    load_dotenv()
    assistant_id = os.getenv("ASSISTANT_ID")
    api_key = os.getenv("OPENAI_API_KEY")
    assistant_client = AssistantClient(api_key=api_key, assistant_id=assistant_id)

    # Create a new thread for the conversation
    thread = assistant_client.create_thread()
    st.session_state.thread_id = thread.id
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # If assistant interaction has not started, ask predefined questions
    if not st.session_state.assistant_started:
        if st.session_state.current_question_index < len(predefined_questions):
            question = predefined_questions[st.session_state.current_question_index]
            with st.chat_message("assistant"):
                display_typing_effect(question)
                # st.markdown(question)

            if user_answer := st.chat_input("Message"):
                st.session_state.predefined_responses.append(user_answer)
                st.session_state.messages.append({"role": "assistant", "content": question})
                st.session_state.messages.append({"role": "user", "content": user_answer})
                st.session_state.current_question_index += 1

                with st.chat_message("user"):
                    st.markdown(user_answer)

                time.sleep(0.5)
                st.rerun()
        else:
            # Once all predefined questions are answered, provide the gathered information to the assistant
            with st.chat_message("assistant"):
                with st.spinner('Initializing...'):
                    initial_data = "Here is some data to start the conversation in the background: ... \
                                    Now, thank the user for the information and ask a question about the project before\
                                    you genearte an epic"
                    run = assistant_client.submit_message(st.session_state.thread_id, initial_data)
                    run = assistant_client.wait_on_run(run, st.session_state.thread_id)
                    response_messages = assistant_client.get_response_messages(st.session_state.thread_id)
                    initial_response = assistant_client.extract_assistant_response(response_messages)
                
                display_typing_effect(initial_response)
                st.session_state.messages.append({"role": "assistant", "content": initial_response})
                st.session_state.assistant_started = True
                st.rerun()

    else:
        # Assistant interaction has started, allow user to chat with the assistant
        if user_query := st.chat_input("Message"):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):
                with st.spinner(''):
                    run = assistant_client.submit_message(st.session_state.thread_id, user_query)
                    run = assistant_client.wait_on_run(run, st.session_state.thread_id)
                    response_messages = assistant_client.get_response_messages(st.session_state.thread_id)
                    response = assistant_client.extract_assistant_response(response_messages)
                    # st.markdown(response)
                    
                display_typing_effect(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
