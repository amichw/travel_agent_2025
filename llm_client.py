import os
import json
from types import GeneratorType
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
        - JSON mode ALWAYS disables streaming.
        - stream=True returns a generator only for main assistant responses.
        - stream=False ALWAYS returns a final string.
        """

        # JSON mode MUST disable streaming
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

        # -----------------------------------------------------------
        # STREAMING MODE (normal assistant responses)
        # -----------------------------------------------------------
        if stream:
            # Return a clean generator for streaming
            def generator():
                for chunk in completion:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
            return generator()

        # -----------------------------------------------------------
        # NON-STREAM MODE
        # But Groq sometimes returns a generator anyway → handle it!
        # -----------------------------------------------------------
        if isinstance(completion, GeneratorType):
            # Unexpected generator → consume fully
            text = ""
            for chunk in completion:
                delta = chunk.choices[0].delta.content
                if delta:
                    text += delta
            return text

        # Normal response object
        content = completion.choices[0].message.content

        # -----------------------------------------------------------
        # JSON MODE PARSING
        # -----------------------------------------------------------
        if json_mode:
            try:
                return json.loads(content)
            except Exception:
                return {}

        return content
