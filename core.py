import json, os

USER_FILE = "users.json"

CURRENT_USER = {"id": None, "difficulty": "normal"}

TIME_BY_DIFF = {
    "easy": 60,
    "normal": 45,
    "hard": 30
}

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def login(uid):
    users = load_users()
    if uid not in users:
        users[uid] = {"scores": {}}
        save_users(users)
    CURRENT_USER["id"] = uid
    return True

def save_score(game, score):
    users = load_users()
    uid = CURRENT_USER["id"]
    best = users[uid]["scores"].get(game, 0)
    if score > best:
        users[uid]["scores"][game] = score
    save_users(users)

def get_ranking(game):
    users = load_users()
    rank = []
    for u in users:
        s = users[u]["scores"].get(game, 0)
        rank.append((u, s))
    return sorted(rank, key=lambda x: x[1], reverse=True)
