import json
import os

STORAGE_FILE = "local_store.json"


def load_local_store():

    if not os.path.exists(STORAGE_FILE):
        return []

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:
        print(f"LOAD STORAGE ERROR: {e}")
        return []


def save_local_store(local_store):

    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            json.dump(local_store, file, indent=4)
            file.flush()
            os.fsync(file.fileno())

    except Exception as e:
        print(f"SAVE STORAGE ERROR: {e}")