import json
from llm_client import LLMClient


class IntentRouter:
    def __init__(self, client: LLMClient):
        self.client = client

    def determine_intent(self, user_input: str) -> dict:
        """
        Analyzes the user input to decide which tool (if any) to use.
        Returns a dictionary with 'tool' and 'location'.
        """

        # 1. The Router Prompt
        # We give the LLM strict instructions on how to categorize inputs.
        system_instruction = """
        You are a Router for a travel assistant. Analyze the user's query.

        Available Tools:
        1. "weather": Use for current conditions, rain check, packing for specific weather.
        2. "attractions": Use for "what to do", "places to visit", "sightseeing".
        3. "chat": Use for greetings, history, general advice, or if no location is specified.

        Output Instructions:
        - Return strictly valid JSON.
        - Format: {"tool": "tool_name", "location": "city_name_or_null"}
        - If the user doesn't mention a specific city, use "chat".
        """

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ]

        # 2. Call LLM in JSON Mode
        # We use the client we built in Component 1
        try:
            response_dict = self.client.chat(messages, json_mode=True)
            return response_dict
        except Exception as e:
            print(f"⚠️ Router Error: {e}")
            # Default fallback if JSON parsing fails
            return {"tool": "chat", "location": None}


# --- QUICK TEST BLOCK ---
if __name__ == "__main__":
    # Initialize Client and Router
    client = LLMClient()
    router = IntentRouter(client)

    # Test Cases
    queries = [
        "Hi, who are you?",  # Should be 'chat'
        "Is it raining in Tokyo right now?",  # Should be 'weather' -> 'Tokyo'
        "Give me 3 things to see in London.",  # Should be 'attractions' -> 'London'
        "I want to go to France."  # Ambiguous, likely 'chat' or 'attractions'
    ]

    print("--- Testing Router Logic ---")
    for q in queries:
        decision = router.determine_intent(q)
        print(f"Query: '{q}'\nDecision: {decision}\n")