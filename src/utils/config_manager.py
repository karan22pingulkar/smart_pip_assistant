import os
import json


class ConfigManager:

    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path

        self.default_settings = {
            "width": 400,
            "height": 250,
            "x_position": 100,
            "y_position": 100,
            "opacity": 0.9,
            "always_on_top": True
        }

        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

    def load_settings(self) -> dict:
        """Reads settings from the JSON file. Falls back to defaults if missing or broken."""
        if not os.path.exists(self.config_path):
            self.save_settings(self.default_settings)
            return self.default_settings

        try:
            with open(self.config_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("[Warning] Settings file corrupted. Resetting to defaults.")
            return self.default_settings

    def save_settings(self, settings: dict) -> bool:
        """Saves the current settings dictionary back to the JSON file."""
        try:
            with open(self.config_path, "w") as file:
                json.dump(settings, file, indent=4)
            return True
        except IOError as e:
            print(f"[Error] Failed to save settings: {e}")
            return False
