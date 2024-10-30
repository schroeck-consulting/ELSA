#  _____      _                         _      _____ _____   _____                       _ _   _
# /  ___|    | |                       | |    |_   _|_   _| /  __ \                     | | | (_)
# \ `--.  ___| |__  _ __ ___   ___  ___| | __   | |   | |   | /  \/ ___  _ __  ___ _   _| | |_ _ _ __   __ _
#  `--. \/ __| '_ \| '__/ _ \ / _ \/ __| |/ /   | |   | |   | |    / _ \| '_ \/ __| | | | | __| | '_ \ / _` |
# /\__/ / (__| | | | | | (_) |  __/ (__|   <   _| |_  | |   | \__/\ (_) | | | \__ \ |_| | | |_| | | | | (_| |
# \____/ \___|_| |_|_|  \___/ \___|\___|_|\_\  \___/  \_/    \____/\___/|_| |_|___/\__,_|_|\__|_|_| |_|\__, |
#                                                                                                       __/ |
#                                                                                                      |___/

import time
import streamlit as st

from openai import OpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock 



class AssistantClient:

    def __init__(self, api_key: str, assistant_id: str):
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id

    def create_thread(self):
        return self.client.beta.threads.create()

    def submit_message(self, thread_id, user_message: str):
        self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )

    def wait_on_run(self, run, thread_id):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run

    def get_response_messages(self, thread_id):
        return self.client.beta.threads.messages.list(thread_id=thread_id,
                                                      order="asc")

    def extract_assistant_response(self, messages) -> str:
        """
        Extracts the most recent assistant response from the messages.
        """
        message_list = list(messages)
        for m in reversed(message_list):
            if m.role == "assistant":
                return m.content[0].text.value
        return ""
    
    
    def add_query_to_thread(self, thread_id, query):
        '''
        Adds a user query to the thread.
        '''
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=query
            )
        
    def stream_assistant_response(self, thread_id):
        stream = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id,
                stream=True
                )
            
        assistant_reply_box = st.empty()
        assistant_reply = ""

        for event in stream:
            # we only consider the streaming events with a delta text
            if isinstance(event, ThreadMessageDelta):
                if isinstance(event.data.delta.content[0], TextDeltaBlock):
                    assistant_reply_box.empty()
                    assistant_reply += event.data.delta.content[0].text.value
                    assistant_reply_box.markdown(assistant_reply)

        return assistant_reply