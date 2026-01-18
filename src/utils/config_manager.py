import os
import json


class ConfigManager:
    def __init__(self, filename="window_settings.json"):
        self.filepath = os.path.join(os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))), filename)

    def load_settings(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_settings(self, settings):
        try:
            with open(self.filepath, "w") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving window layout config state metrics: {e}")
