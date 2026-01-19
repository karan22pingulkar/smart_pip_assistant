import sys
import os
import json
import socketio
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from utils.config_manager import ConfigManager
from core.pip_window import PipWindow

# Fallback defaults if config file is absent
DEFAULT_URL = "https://your-pip-project.onrender.com"

# Correct path lookup matching your project setup root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(BASE_DIR, "config.json")

if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            CLOUD_SERVER_URL = json.load(f).get(
                "CLOUD_SERVER_URL", DEFAULT_URL)
    except Exception:
        CLOUD_SERVER_URL = DEFAULT_URL
else:
    CLOUD_SERVER_URL = DEFAULT_URL


class CloudBridge(QObject):
    url_received = pyqtSignal(str)


cloud_bridge = CloudBridge()
sio = socketio.Client()


@sio.event
def connect():
    print("[Cloud] Connected to the real-time cloud network successfully!")


@sio.on('video_signal')
def on_video_signal(data):
    video_url = data.get('url')
    if video_url:
        print(f"[Cloud] Received incoming streaming payload: {video_url}")
        # Safe thread handoff over to our running PyQt6 UI
        cloud_bridge.url_received.emit(video_url)


@sio.event
def disconnect():
    print("[Cloud] Connection lost from cloud platform.")


def start_websocket():
    try:
        sio.connect(CLOUD_SERVER_URL)
    except Exception as e:
        print(f"[Error] Network connection handshake dropped: {e}")


def main():
    app = QApplication(sys.argv)

    config = ConfigManager()
    window = PipWindow(config)

    # When a cloud signal fires, update layout and reveal frame
    cloud_bridge.url_received.connect(
        lambda url: [window.load_url(url), window.show()])

    print(
        f"[Connecting] Initiating WebSocket link connection to: {CLOUD_SERVER_URL}")
    start_websocket()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
