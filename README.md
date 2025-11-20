 Voyager — Travel Assistant (LLM Project)

Voyager is a conversation-first travel assistant built to demonstrate effective LLM prompt design, intent routing, tool integration, and contextual dialogue management. The system maintains natural multi-turn conversations while blending external data such as weather and attraction information.

## Features
- Natural, travel-focused conversation flow  
- Intent router (weather / attractions / general travel chat) powered by JSON-mode LLM  
- External tools: live weather API + attraction lookup  
- Structured system prompts with hidden CoT reasoning  
- Full conversation context handling with sliding window memory  
- Hallucination-mitigation layer via reflection pass  
- Full event logging of the reasoning+tool pipeline for later analysis  

## Running the Assistant
```
export GROQ_TRAVEL_API_KEY="..."
export OPENWEATHER_API_KEY="..."
python assistant.py
```

## Testing
A dedicated test harness simulates 10 conversations and logs full traces.  
Optional LLM analysis evaluates:
- conversation quality  
- domain adherence  
- hallucination risk  
- improvement suggestions  

## Project Structure
```
assistant.py        – orchestration loop + streaming
llm_client.py       – Groq wrapper with JSON-safe routing
router.py           – intent classification via LLM
state_manager.py    – multi-turn context memory
tools.py            – weather + attractions tools
prompts.py          – system, CoT, router, reflection prompts
reflection.py       – hallucination mitigation
utils.py            – logger + formatting helpers
test_conversations.py – simulations + analysis
```

## Visual Architecture Diagram

```
                          ┌────────────────────────┐
                          │        User Input       │
                          └─────────────┬──────────┘
                                        │
                                        ▼
                          ┌────────────────────────┐
                          │     TravelAssistant     │
                          │  (Main Orchestrator)   │
                          └─────────────┬──────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
 ┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
 │  StateManager     │        │   IntentRouter   │        │    EventLogger   │
 │ (conversation mem)│        │ (weather/POI/chat)│       │ (full trace log) │
 └─────────┬────────┘        └──────────┬────────┘        └──────────┬──────┘
           │                             │                            │
           │                             ▼                            │
           ▼                 ┌──────────────────────┐                  ▼
 ┌──────────────────┐        │ LLMClient (Groq API) │        ┌──────────────────┐
 │  prompts.py       │       └──────────┬───────────┘        │ reflection.py     │
 │ (System,CoT,Router)│                │                     │ (hallucination fix)│
 └──────────────────┘                  │                     └──────────────────┘
                                        ▼
                          ┌────────────────────────┐
                          │    Final Assistant      │
                          │       Response          │
                          └────────────────────────┘
```

## Short Notes on Key Prompt Engineering Decisions

1. **Strict but natural travel-domain persona**  
   The system prompt constrains the assistant to travel topics while keeping replies natural and friendly. Ambiguous messages are interpreted in travel context.

2. **Hidden Chain-of-Thought**  
   Included only as a system instruction to improve internal reasoning.

3. **LLM Router With Few-Shot Examples**  
   Makes routing accurate and deterministic.

4. **Structured Tool Context Injection**  
   Wrapping tool data in `<tool_context>` ensures grounded responses.

5. **Reflection Pass**  
   A separate model pass reviews and corrects potential hallucinations.

6. **Context Management**  
   Sliding-window memory balances coherence and token efficiency.

7. **Error Handling Philosophy**  
   - Router fallback to chat  
   - Mock data when APIs fail  
   - Clarifying questions over guessing  
   - Full event logging at each step