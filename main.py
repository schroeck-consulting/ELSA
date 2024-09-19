import streamlit as st
import os
from dotenv import load_dotenv
from assistant_api import AssistantClient
from utils import display_typing_effect


def init_session_state():
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o-2024-08-06"
    if "messages" not in st.session_state:
        st.session_state.messages = []


def main():
    st.title("Epic Builder Copilot")

    init_session_state()

    # Initialize OpenAI Assistant Client
    load_dotenv()
    assistant_id = os.getenv("ASSISTANT_ID")
    api_key = os.getenv("OPENAI_API_KEY")
    assistant_client = AssistantClient(api_key=api_key, assistant_id=assistant_id) 
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if user_query := st.chat_input("Message"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner(''):
                thread = assistant_client.create_thread()
                run = assistant_client.submit_message(thread, user_query)
                run = assistant_client.wait_on_run(run, thread)
                response_messages = assistant_client.get_response_messages(thread)
                response = assistant_client.extract_assistant_response(response_messages)
                # st.markdown(response)
                
            # Simulate typing effect
            display_typing_effect(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
