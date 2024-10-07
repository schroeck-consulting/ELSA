import time
from openai import OpenAI

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
        return self.client.beta.threads.messages.list(thread_id=thread_id, order="asc")
    

    def extract_assistant_response(self, messages) -> str:
        """
        Extracts the most recent assistant response from the messages.
        """
        message_list = list(messages)
        for m in reversed(message_list):
            if m.role == "assistant":
                return m.content[0].text.value
        return ""
