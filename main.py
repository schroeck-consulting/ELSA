import streamlit as st
import os
import time
from openai import OpenAI
from dotenv import load_dotenv


def pretty_print(messages):
    responses = []
    for m in messages:
        if m.role == "assistant":
            responses.append(m.content[0].text.value)
    return "\n".join(responses)

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(os.getenv("ASSISTANT_ID"), thread, user_input)
    return thread, run

######
st.title("Epic Builder Copilot")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-2024-08-06"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Message"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner('Processing...'):
            thread = client.beta.threads.create()
            run = submit_message(os.getenv("ASSISTANT_ID"), thread, user_query)
            run = wait_on_run(run, thread)
            response_messages = get_response(thread)
            response = pretty_print(response_messages)
            # st.markdown(response)
            
        # Simulate typing effect
        message_placeholder = st.empty()
        full_response = ""
        for char in response:
            full_response += char
            message_placeholder.markdown(full_response)
            time.sleep(0.002)  # Adjust the speed as needed
    st.session_state.messages.append({"role": "assistant", "content": response})
