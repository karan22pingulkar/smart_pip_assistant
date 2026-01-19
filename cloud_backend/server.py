import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
# Initialize Socket.IO with CORS allowed for the extension and desktop client app
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def home():
    return "Cloud PiP Signalling Server Active!", 200

# Endpoint where the Chrome Extension will POST the incoming video link


@app.route('/open-pip', methods=['POST'])
def open_pip():
    data = request.get_json()
    video_url = data.get('url')
    if video_url:
        print(f"[Cloud] Broadcasting URL to desktop client: {video_url}")
        # Broadcast the payload in real-time to any connected Python desktop apps
        socketio.emit('video_signal', {'url': video_url})
        return jsonify({"status": "broadcasted"}), 200
    return jsonify({"status": "error"}), 400


if __name__ == "__main__":
    # Render sets the PORT environment variable automatically
    port = int(os.environ.get("PORT", 5000))

    # Standard production WSGI deployment engine wrapper configuration
    socketio.run(app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True)
