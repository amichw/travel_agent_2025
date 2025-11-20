# assistant.py

from llm_client import LLMClient
from state_manager import StateManager
from router import IntentRouter
from tools import AVAILABLE_TOOLS
from utils import (
    EventLogger,
    format_weather_payload,
    format_attractions_payload
)
from prompts import SYSTEM_PROMPT, COT_PROMPT
from reflection import apply_reflection


class TravelAssistant:
    def __init__(self):
        self.llm = LLMClient()
        self.state = StateManager(system_prompt=SYSTEM_PROMPT)
        self.router = IntentRouter(self.llm)
        self.logger = EventLogger()

    def run_turn(self, user_msg: str):
        """
        Execute a full interaction turn with:
        - intent routing
        - tool execution
        - prompt construction
        - LLM streaming response
        - reflection
        - event logging at every step
        """
        # Log user input
        self.logger.log("user_input", {"text": user_msg})

        # Save to state
        self.state.add_user(user_msg)

        # ------------ INTENT ROUTING ------------
        intent = self.router.determine_intent(user_msg)
        self.logger.log("router_decision", intent)

        tool = intent.get("tool")
        location = intent.get("location")

        tool_context_text = None

        # ------------ TOOL LOGIC ------------
        if tool in AVAILABLE_TOOLS and location:
            self.logger.log("tool_call", {"tool": tool, "location": location})

            raw_output = AVAILABLE_TOOLS[tool](location)
            self.logger.log("tool_raw_output", raw_output)

            # Format tool output so the LLM can use it well
            if tool == "weather":
                tool_context_text = format_weather_payload(raw_output)
            elif tool == "attractions":
                tool_context_text = format_attractions_payload(raw_output)
            else:
                tool_context_text = str(raw_output)

            self.logger.log("tool_formatted_context", {"text": tool_context_text})

        # ------------ BUILD LLM PROMPT ------------
        messages = self.state.build_messages(
            cot_prompt=COT_PROMPT,
            tool_context=tool_context_text
        )

        self.logger.log("prompt_to_llm", {"messages": messages})

        # ------------ STREAM LLM RESPONSE ------------
        print("\nAssistant:")
        final_text = ""

        for chunk in self.llm.chat(messages, stream=True, temperature=0.4):
            final_text += chunk
            print(chunk, end="", flush=True)

        # Log each streaming chunk  NOPE
        self.logger.log("llm_stream_chunks", {"all chunks": final_text})

        # ------------ REFLECTION / SAFETY PASS ------------
        reflection = apply_reflection(self.llm, final_text)
        self.logger.log("reflection_output", {"reflection": reflection})

        # Save final assistant output
        self.state.add_assistant(reflection)
        self.logger.log("assistant_final", {"text": reflection})

        print("\n" + "-" * 60)

        return reflection  # optional, useful for testing harness


if __name__ == "__main__":
    bot = TravelAssistant()

    while True:
        user = input("You: ")
        if user.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        bot.run_turn(user)
    bot.logger.save()
