# state_manager.py

class StateManager:
    def __init__(self, system_prompt: str, max_turns=8):
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.history = []

    def add_user(self, msg):
        self.history.append({"role": "user", "content": msg})

    def add_assistant(self, msg):
        self.history.append({"role": "assistant", "content": msg})

    def build_messages(self, cot_prompt, tool_context=None):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": cot_prompt}
        ]

        # Sliding window
        recent = self.history[-(self.max_turns * 2):]
        messages.extend(recent)

        if tool_context:
            messages.append({
                "role": "system",
                "content": f"<tool_context>{tool_context}</tool_context>"
            })

        return messages

    def update_system_prompt(self, new_prompt: str):
        """Useful if you want to change the persona dynamically."""
        self.system_prompt = new_prompt


# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    # 1. Initialize with a persona
    state = StateManager(system_prompt="You are a helpful travel guide.")

    # 2. Simulate a conversation
    state.add_user("I want to go to Tokyo.")
    state.add_assistant("Tokyo is amazing! When are you planning to go?")
    state.add_user("Next week. What should I pack?")

    # 3. Test Normal Retrieval
    print("--- Normal Request ---")
    print(state.build_messages())

    # 4. Test Context Injection (The "Weather" Scenario)
    print("\n--- Request with Weather Context ---")
    weather_data = "Current Weather in Tokyo: 5°C, Heavy Rain."
    final_payload = state.get_messages_for_llm(temporary_context=weather_data)

    # Print nicely to see the structure
    import json
    print(json.dumps(final_payload, indent=2))