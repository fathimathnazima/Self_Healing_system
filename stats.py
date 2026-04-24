import json
import os
from datetime import datetime

STATS_FILE = "stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

def update_failure(service_name):
    stats = load_stats()

    if service_name not in stats:
        stats[service_name] = {
            "failures": 0,
            "last_restart": None
        }

    stats[service_name]["failures"] += 1
    stats[service_name]["last_restart"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_stats(stats)

def update_last_seen(service_name):
    stats = load_stats()

    if service_name not in stats:
        stats[service_name] = {}

    stats[service_name]["last_seen"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_stats(stats)

def get_stats(service_name):
    stats = load_stats()
    return stats.get(service_name, {"failures": 0})

def get_risk_level(failures):
    if failures <= 2:
        return "LOW"
    elif failures <= 5:
        return "MEDIUM"
    else:
        return "HIGH"

def is_unstable(failures):
    return failures >= 3