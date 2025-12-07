import json
import os

FILE = "healthbackend/storage/history.json"

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save(data):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_history(user_id, entry):
    data = load()
    data.setdefault(user_id, []).append(entry)
    save(data)

def get_history(user_id):
    return load().get(user_id, [])
