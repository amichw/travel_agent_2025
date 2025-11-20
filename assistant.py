from llm_client import LLMClient
from state_manager import StateManager
from router import IntentRouter
from tools import AVAILABLE_TOOLS


class TravelAssistant:
    def __init__(self, system_prompt: str):
        # Initialize all four components
        self.llm_client = LLMClient()
        self.state_manager = StateManager(system_prompt=system_prompt)
        self.router = IntentRouter(self.llm_client)

    def process_query(self, user_query: str):
        """
        The main orchestration loop for a single user turn.
        """
        # 1. Add user query to history
        self.state_manager.add_user_message(user_query)

        tool_context = None

        # 2. Call the Router to determine intent
        try:
            decision = self.router.determine_intent(user_query)
            tool_name = decision.get("tool")
            location = decision.get("location")
        except Exception:
            # Router fallback
            tool_name = "chat"
            location = None

        print(f"🤖 [ORCHESTRATOR] Router decision: Tool={tool_name}, Location={location}")

        # 3. Tool Execution (The 'RAG' / Data Augmentation step)
        if tool_name in AVAILABLE_TOOLS and location:
            tool_func = AVAILABLE_TOOLS[tool_name]
            print(f"⚙️ [TOOL] Calling {tool_name} for {location}...")

            # Execute the external function
            raw_tool_output = tool_func(location)

            # Format tool output for the LLM
            tool_context = f"The {tool_name} tool provided this real-time data: {raw_tool_output}"

        # 4. Final Prompt Preparation & CoT Injection

        # Inject the CoT instruction right before the user message for the best result
        cot_instruction = """
        STEP-BY-STEP INSTRUCTION (Chain-of-Thought):
        1. Acknowledge the user's latest message.
        2. IF tool data exists (CONTEXT DATA below), explicitly use it to answer the question, but do NOT mention the tool was called.
        3. IF the conversation history provides necessary context, reference it.
        4. Provide the final, friendly travel assistant response.
        5. Ask a follow up question
        """

        # Get the full history, including the temporary tool context
        messages_payload = self.state_manager.get_messages_for_llm(
            temporary_context=tool_context
        )

        # Inject CoT into the system prompt for high-quality reasoning
        messages_payload[0]['content'] = cot_instruction + "\n\n" + messages_payload[0]['content']

        # 5. Final LLM Call (Streaming to the user)
        print("\n✨ [ASSISTANT] Final Answer:")

        assistant_response = ""

        # Use streaming for a responsive UI experience
        for chunk in self.llm_client.chat(messages_payload, stream=True):
            print(chunk, end="", flush=True)
            assistant_response += chunk

        print("\n---")

        # 6. Save Assistant's final answer to history
        self.state_manager.add_assistant_message(assistant_response)


### 3. Execution (The Chat Loop)
if __name__ == "__main__":
    # The main system prompt (the assistant's persona)
    SYSTEM_PROMPT = "You are a friendly and knowledgeable travel assistant named 'Voyager'. You always keep your answers concise and useful."

    assistant = TravelAssistant(SYSTEM_PROMPT)

    # Start the interactive chat
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("👋 Goodbye!")
            break

        # Execute the full orchestration flow
        assistant.process_query(user_input)

