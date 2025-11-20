# llm_client.py
import os
import json
from groq import Groq

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_TRAVEL_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GROQ_TRAVEL_API_KEY environment variable.")

        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"

    def chat(self, messages, stream=False, json_mode=False, temperature=0):
        """
        Wrapper for Groq chat completion.
        JSON mode is *always* non-streaming.
        Streaming is only allowed for normal chat.
        """

        # JSON mode MUST disable streaming to avoid generator errors
        if json_mode:
            stream = False

        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }

        if json_mode:
            params["response_format"] = {"type": "json_object"}

        completion = self.client.chat.completions.create(**params)

        # STREAM MODE (only allowed when json_mode=False)
        if stream:
            for chunk in completion:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            return  # generator mode

        # NON-STREAM MODE
        content = completion.choices[0].message.content

        if json_mode:
            try:
                return json.loads(content)
            except Exception:
                return {}
        else:
            return content
