# storage/json_storage.py
import json
import os

class JSONStorage:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
