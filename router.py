# router.py
from llm_client import LLMClient
from prompts import ROUTER_PROMPT

class IntentRouter:
    def __init__(self, client: LLMClient):
        self.client = client

    def determine_intent(self, user_input: str) -> dict:
        """
        The router MUST always call the LLM in JSON mode
        and MUST NOT stream under any circumstances.
        """

        messages = [
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": user_input}
        ]

        try:
            result = self.client.chat(
                messages,
                json_mode=True,       # ALWAYS JSON
                stream=False,         # NEVER STREAM
                temperature=0         # Deterministic
            )

            # Ensure valid structure
            if isinstance(result, dict):
                return result
            else:
                return {"tool": "chat", "location": None}

        except Exception as e:
            print(f"[Router Error]: {e}")
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
