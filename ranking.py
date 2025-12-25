import json
import os

FILE = "ranking.json"

def load_rank():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_score(name, score):
    data = load_rank()
    data.append({"name": name, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
