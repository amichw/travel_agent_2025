# test_conversations.py

import json
import datetime
from assistant import TravelAssistant
from llm_client import LLMClient

TEST_CONVERSATIONS = [
    # Travel queries
    ["Hi", "I want to go somewhere warm in March", "What should I pack?", "Any good food there?"],
    ["I'm visiting Tokyo next week", "What’s the weather like?", "What are some attractions nearby?"],
    ["Planning a weekend trip to Paris", "Where should I stay?", "Any hidden gems I shouldn't miss?"],
    ["I want to relax", "Which destinations are best for beaches?", "How expensive is it?"],
    ["Give me ideas for a 3-day family trip in Italy", "Activities for kids?", "Where to base?"],

    # Ambiguous travel-like inputs
    ["I want pizza", "Where can I get good pizza while traveling?", "Anything else to do nearby?"],
    ["I'm bored", "What can I do in my area when traveling?", "Any recommended attractions?"],
    ["I'm cold", "Where is warm this time of year?", "Packing suggestions?"],

    # Edge-case / off-topic redirects
    ["Tell me a joke", "Okay but focus on travel", "Suggest a fun destination"],
    ["My cat is cute", "Anyway, back to travel… What's a good destination for nature lovers?"]
]


def run_simulation():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot = TravelAssistant()
    logs = {"timestamp": timestamp, "runs": []}

    print("\n=== Running 10 Conversation Simulations ===\n")

    for i, convo in enumerate(TEST_CONVERSATIONS):
        print(f"\n--- Conversation {i + 1} ---")
        convo_log = {"id": i + 1, "turns": []}

        for user_msg in convo:
            print(f"\nUser: {user_msg}")
            convo_log["turns"].append({"user": user_msg})

            # Capture assistant response instead of printing only
            response = capture_assistant_output(bot, user_msg)
            convo_log["turns"][-1]["assistant"] = response

        logs["runs"].append(convo_log)
    bot.logger.save()
    OUTPUT_FILE = f"test_logs_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Test results saved to: {OUTPUT_FILE}\n")
    return logs


def capture_assistant_output(bot, user_msg):
    """Utility: run a turn but capture printed streaming output."""
    from io import StringIO
    import sys

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()

    bot.run_turn(user_msg)

    sys.stdout = old_stdout
    output = buffer.getvalue()

    # Clean up stream output (remove separators)
    cleaned = output.replace("Assistant:", "").replace("------------------------------------------------------------",
                                                       "")
    return cleaned.strip()


def analyze_with_llm(log_data):
    """
    Optional: Ask the LLM to analyze all 10 conversations
    and produce the structured report.
    """
    print("\n=== Sending Logs to LLM for Analysis ===\n")

    client = LLMClient()

    messages = [
        {
            "role": "system",
            "content":
                """
                You are a senior AI evaluator. Analyze each conversation from a travel assistant
                for quality, relevance, tone, hallucination risk, and travel-domain adherence.

                For each conversation, provide:
                - Quality score (0–10)
                - Accuracy score
                - Travel-domain consistency score
                - Notes on tone, naturalness, and helpfulness
                - Any hallucinations detected
                - What the assistant could improve

                Return structured markdown with headers.
                """
        },
        {
            "role": "user",
            "content": json.dumps(log_data, indent=2, ensure_ascii=False)
        }
    ]
    # Always returns a STRING now
    report_text = client.chat(
        messages,
        stream=False,  # force non-streaming
        json_mode=False,  # needed for safe eval mode
        temperature=0.2
    )

    OUTPUT_FILE = f"test_analysis_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n✓ Analysis saved to: {OUTPUT_FILE}\n")
    return report_text


if __name__ == "__main__":
    logs = run_simulation()
    gen_report = analyze_with_llm(logs)


    run_analysis = input("\nRun LLM analysis? (y/n): ").strip().lower()
    if run_analysis == "y":
        gen_report = analyze_with_llm(logs)
        print(gen_report)

