import json
import os

FILE = "users.json"

def load_users():
    if not os.path.exists(FILE):
        return {}
    return json.load(open(FILE, "r", encoding="utf-8"))

def login(name):
    users = load_users()
    if name not in users:
        users[name] = {}
    json.dump(users, open(FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return name
