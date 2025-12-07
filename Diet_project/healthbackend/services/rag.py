import json
import os

KB_PATH = "data/knowledge.json"

def retrieve_context(query: str, top_k: int = 2) -> str:
    if not os.path.exists(KB_PATH):
        return ""

    with open(KB_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    query_l = query.lower()
    hits = []

    for doc in docs:
        if any(word in doc["content"].lower() for word in query_l.split()):
            hits.append(doc["content"])

    return "\n".join(hits[:top_k])
