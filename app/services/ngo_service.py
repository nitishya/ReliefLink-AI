import json
import os

def get_ngo_dataset():
    path = os.path.join(os.path.dirname(__file__), "../../data/ngos.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading NGO data: {e}")
        return []

def get_ngo_dataset_str():
    dataset = get_ngo_dataset()
    return json.dumps(dataset)
