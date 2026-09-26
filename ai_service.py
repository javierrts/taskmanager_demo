import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AIService:
    """Wraps calls to the Gemini API using its OpenAI-compatible endpoint."""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set. Add it to your .env file.")
        self.client = OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
        )

    def ask(self, prompt: str, model: str = "gemini-3.8-flash") -> str:

        params = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a expert task management assistant, that helps break down tasks into simpler subtasks."},
                {"role": "user", "content": prompt}
            ],  
            "max_tokens": 300,
            "reasoning_effort": "low",
        }
        response = self.client.chat.completions.create(**params)

        content = response.choices[0].message.content.strip()

        subtasks = []
        for line in content.split("\n"):
            if line.strip() and line.startswith("-"):
                subtasks.append(line[1:].strip())

        return subtasks if subtasks else ["Error: No subtasks found."]


    def create_simple_task_from_complex(self, description):
        prompt = f"""Divide this task in 3 or 5 subtask more simple and affordable.
        Task: {description}
        Response format
         - Subtask 1
         - Subtask 2
         - Subtask 3

         response only with subtasks list, one per line, with a - at the beginning of each line.
        """
        return self.ask(prompt)