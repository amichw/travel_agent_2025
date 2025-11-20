# Voyager — AI Travel Assistant (LLM Project)

A conversation-first AI travel assistant designed to showcase:

✔ Prompt engineering  
✔ Multi-turn context  
✔ Tool integration (weather + attractions)  
✔ Intent routing  
✔ Reflection-based hallucination checking  
✔ Clean LLM architecture  

---

## Features

### 🔹 Advanced Prompt Engineering
- Centralized prompts (`prompts.py`)
- Hidden chain-of-thought
- Reflection layer
- Anti-hallucination protections

### 🔹 External Tooling
- Weather API (OpenWeather)
- Simple Attractions tool (mock or extendable)
- Automatic tool selection via LLM router

### 🔹 Robust Architecture
- StateManager → conversation memory  
- IntentRouter → deterministic action selection  
- LLMClient → Groq API wrapper  
- TravelAssistant → business orchestration  

---

## Run the Assistant

export GROQ_TRAVEL_API_KEY="YOUR_KEY"
export OPENWEATHER_API_KEY="YOUR_KEY" 

---

## Sample Conversation

**You:** "Is it raining in Tokyo right now?"  
**Voyager:** "Right now Tokyo is 22°C and partly cloudy. Are you planning an outdoor activity?"

---

## Project Structure

assistant.py
llm_client.py
router.py
state_manager.py
tools.py
prompts.py
reflection.py
utils.py
README.md

---

## Why This Project Stands Out

- Clean, modular LLM design  
- Demonstrates real-world LLM engineering  
- Avoids hallucinations using reflection  
- Deterministic routing using JSON LLM tool  
- Multi-turn conversation with context  

---

## Extendable

Ideas:
- Add currency conversion  
- Add hotel recommendations  
- Connect OpenTripMap  
- Add user preference memory  
