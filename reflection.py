# reflection.py

from prompts import REFLECTION_PROMPT

def apply_reflection(llm_client, assistant_answer):
    messages = [
        {"role": "system", "content": REFLECTION_PROMPT},
        {"role": "user", "content": assistant_answer}
    ]
    return llm_client.chat(messages, stream=False, temperature=0.1)
