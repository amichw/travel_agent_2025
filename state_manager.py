from typing import List, Dict, Optional
import json


class StateManager:
    def __init__(self, system_prompt: str, max_history: int = 10):
        """
        max_history: Number of exchanges (User + AI pairs) to keep.
        """
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []

    def add_user_message(self, content: str):
        self.history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.history.append({"role": "assistant", "content": content})

    def get_messages_for_llm(self, temporary_context: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Prepares the final list of messages to send to the LLM.

        Logic:
        1. Start with the System Prompt.
        2. Add the Sliding Window of recent history.
        3. (Optional) Inject temporary context (like Weather) as a 'system' update
           right before the latest user message, or strictly as the latest system instruction.
        """

        # 1. Enforce Sliding Window (keep last N messages)
        # We multiply by 2 because 1 interaction = 1 User + 1 Assistant
        current_history = self.history[-self.max_history * 2:]

        # 2. Construct the base message list
        messages = [{"role": "system", "content": self.system_prompt}]

        # 3. Inject Context (The "Augmentation" part of RAG)
        # If we have tool data (e.g., "It is raining in Paris"), we verify
        # the user isn't asking about it, but it's good practice to put it
        # as a high-priority system note just before the end.
        if temporary_context:
            context_message = {
                "role": "system",
                "content": f"CONTEXT DATA (Use this to answer the user's latest question):\n{temporary_context}"
            }
            messages.append(context_message)

        # 4. Add Conversation History
        messages.extend(current_history)

        return messages

    def update_system_prompt(self, new_prompt: str):
        """Useful if you want to change the persona dynamically."""
        self.system_prompt = new_prompt


# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    # 1. Initialize with a persona
    state = StateManager(system_prompt="You are a helpful travel guide.")

    # 2. Simulate a conversation
    state.add_user_message("I want to go to Tokyo.")
    state.add_assistant_message("Tokyo is amazing! When are you planning to go?")
    state.add_user_message("Next week. What should I pack?")

    # 3. Test Normal Retrieval
    print("--- Normal Request ---")
    print(state.get_messages_for_llm())

    # 4. Test Context Injection (The "Weather" Scenario)
    print("\n--- Request with Weather Context ---")
    weather_data = "Current Weather in Tokyo: 5°C, Heavy Rain."
    final_payload = state.get_messages_for_llm(temporary_context=weather_data)

    # Print nicely to see the structure
    print(json.dumps(final_payload, indent=2))