# File: assistant_manager.py

from openai import OpenAI

class AssistantManager:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def create_thread(self):
        """Create a new thread for conversation."""
        thread = self.client.beta.threads.create()
        return thread.id

    def add_message_to_thread(self, thread_id, role, content):
        """Add a message to the specified thread."""
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content
        )

    def run_assistant(self, thread_id, assistant_id):
        """Run the assistant on the specified thread."""
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            model=self.model
        )

        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break

    def get_assistant_response(self, thread_id):
        """Retrieve the assistant's response from the thread."""
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        assistant_messages = [msg for msg in messages if msg.role == 'assistant']
        
        if assistant_messages:
            latest_message = assistant_messages[0]
            return latest_message.content[0].text.value
        else:
            return "No response from the assistant."

    def list_assistants(self):
        """List all available assistants."""
        assistants = self.client.beta.assistants.list()
        return [{"id": asst.id, "name": asst.name} for asst in assistants]

    def create_assistant(self, name, instructions, tools=None):
        """Create a new assistant."""
        assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools or [],
            model=self.model
        )
        return assistant.id

    def delete_assistant(self, assistant_id):
        """Delete an assistant."""
        self.client.beta.assistants.delete(assistant_id)

    def update_assistant(self, assistant_id, **kwargs):
        """Update an existing assistant."""
        self.client.beta.assistants.update(assistant_id, **kwargs)