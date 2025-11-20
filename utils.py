# utils.py

import json
import datetime

def format_weather_payload(d):
    if d["status"] != "ok" and d["status"] != "mock":
        return "Weather unavailable."

    return f"Weather in {d['city']}: {d['temp']}°C, {d['description']}."

def format_attractions_payload(d):
    if not d["items"]:
        return f"No attractions found for {d['city']}."

    text = "\n".join([f"- {i}" for i in d["items"]])
    return f"Top attractions in {d['city']}:\n{text}"


class EventLogger:
    def __init__(self):
        self.events = []

    def log(self, event_type: str, data: dict):
        self.events.append({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "type": event_type,
            "data": data
        })

    def export(self):
        return self.events

    def save(self, path=None):
        if path is None:
            path = f"conversation_trace_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)
