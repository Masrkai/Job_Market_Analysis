import os
import json

CHECKPOINT_FILE = "checkpoint.json"

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return {"country_index": 0, "job_index": 0}

    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"country_index": 0, "job_index": 0}


def save_checkpoint(ci, ji):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(
            {"country_index": ci, "job_index": ji},
            f,
            indent=2
        )