# assistant.py

from llm_client import LLMClient
from state_manager import StateManager
from router import IntentRouter
from tools import AVAILABLE_TOOLS
from utils import format_weather_payload, format_attractions_payload
from prompts import SYSTEM_PROMPT, COT_PROMPT
from reflection import apply_reflection

class TravelAssistant:
    def __init__(self):
        self.llm = LLMClient()
        self.state = StateManager(system_prompt=SYSTEM_PROMPT)
        self.router = IntentRouter(self.llm)

    def run_turn(self, user_msg: str):
        self.state.add_user(user_msg)

        # Routing
        intent = self.router.determine_intent(user_msg)
        tool = intent.get("tool")
        location = intent.get("location")

        tool_context = None

        if tool in AVAILABLE_TOOLS and location:
            raw = AVAILABLE_TOOLS[tool](location)

            if tool == "weather":
                tool_context = format_weather_payload(raw)
            else:
                tool_context = format_attractions_payload(raw)

        # Build messages
        msgs = self.state.build_messages(
            cot_prompt=COT_PROMPT,
            tool_context=tool_context
        )

        # Stream final answer
        print("\nAssistant:")
        final_text = ""
        for chunk in self.llm.chat(msgs, stream=True, temperature=0.4):
            print(chunk, end="", flush=True)
            final_text += chunk

        # Reflection pass (optional, improves hallucination safety)
        safe_final = apply_reflection(self.llm, final_text)

        self.state.add_assistant(safe_final)
        print("\n" + "-"*60)

if __name__ == "__main__":
    bot = TravelAssistant()
    while True:
        user = input("You: ")
        if user.lower() in ("exit", "quit"):
            break
        bot.run_turn(user)
