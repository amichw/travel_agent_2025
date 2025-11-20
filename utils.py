# utils.py

def format_weather_payload(d):
    if d["status"] != "ok" and d["status"] != "mock":
        return "Weather unavailable."

    return f"Weather in {d['city']}: {d['temp']}°C, {d['description']}."

def format_attractions_payload(d):
    if not d["items"]:
        return f"No attractions found for {d['city']}."

    text = "\n".join([f"- {i}" for i in d["items"]])
    return f"Top attractions in {d['city']}:\n{text}"
