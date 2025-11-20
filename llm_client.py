import os
import json
from groq import Groq


class LLMClient:
    def __init__(self):
        # Ensure API Key is set
        self.api_key = os.getenv("GROQ_TRAVEL_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GROQ_TRAVEL_API_KEY environment variable.")

        # Initialize the official client
        self.client = Groq(api_key=self.api_key)

        # Use the latest stable model (fast and cheap/free)
        self.model = "llama-3.1-8b-instant"

    def chat(self, messages, stream=False, json_mode=False):
        """
        Wrapper for Groq chat completion.
        """
        # Prepare arguments
        kwargs = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": 0.7,
        }

        # Enable JSON mode if requested (Crucial for the Router)
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            completion = self.client.chat.completions.create(**kwargs)

            if stream:
                return self._handle_stream(completion)
            else:
                # Standard sync response
                content = completion.choices[0].message.content
                return json.loads(content) if json_mode else content

        except Exception as e:
            print(f"❌ Groq API Error: {e}")
            # Return a safe fallback so the app doesn't crash
            return {} if json_mode else "I'm having trouble connecting to the server."

    def _handle_stream(self, completion):
        """
        Yields chunks of text from the stream generator.
        """
        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content


# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    client = LLMClient()

    print("1. Testing Connection...")
    response = client.chat([{"role": "user", "content": "Say hello!"}])
    print(f"Response: {response}\n")

    print("2. Testing Streaming...")
    for chunk in client.chat([{"role": "user", "content": "Count to 3."}], stream=True):
        print(chunk, end="", flush=True)
    print("\n")

    print("3. Testing JSON Mode...")
    # Note: For JSON mode, you MUST mention 'JSON' in the prompt for Llama 3
    json_prompt = [{"role": "user", "content": "Return a JSON object with a key 'status' set to 'ok'."}]
    json_res = client.chat(json_prompt, json_mode=True)
    print(f"JSON Response: {json_res}")

