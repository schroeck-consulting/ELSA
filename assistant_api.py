import time
from openai import OpenAI

class AssistantClient:

    def __init__(self, api_key: str, assistant_id: str):
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id


    def create_thread(self):
        return self.client.beta.threads.create()
    

    def submit_message(self, thread, user_message: str):
        self.client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        return self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id,
        )
    

    def wait_on_run(self, run, thread):
        while run.status == "queued" or run.status == "in_progress":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        return run
    

    def get_response_messages(self, thread):
        return self.client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    

    def extract_assistant_response(self, messages) -> str:
        responses = []
        for m in messages:
            if m.role == "assistant":
                responses.append(m.content[0].text.value)
        return "\n".join(responses)
    