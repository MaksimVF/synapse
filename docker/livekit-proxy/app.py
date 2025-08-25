




import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
LIVEKIT_JWT_SERVICE_URL = os.getenv("LIVEKIT_JWT_SERVICE_URL", "http://lk-jwt-service:8080")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

@app.route('/generate-token', methods=['POST'])
def generate_token():
    """Generate LiveKit JWT token"""
    data = request.json
    user_id = data.get('user_id')
    room_name = data.get('room_name', '')
    display_name = data.get('display_name', '')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    try:
        response = requests.post(
            f"{LIVEKIT_JWT_SERVICE_URL}/generate",
            json={
                "api_key": LIVEKIT_API_KEY,
                "api_secret": LIVEKIT_API_SECRET,
                "user_id": user_id,
                "room_name": room_name,
                "metadata": {
                    "display_name": display_name,
                },
            },
            timeout=5,
        )
        response.raise_for_status()
        token_data = response.json()
        return jsonify({"token": token_data["token"]})

    except Exception as e:
        logging.error("Failed to generate LiveKit token: %s", e)
        return jsonify({"error": "Failed to generate token"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


