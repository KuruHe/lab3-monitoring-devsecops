import json
import logging
import os
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "lab3-app",
            "message": record.getMessage()
        })

logger = logging.getLogger("lab3-app")
logger.setLevel(logging.INFO)
logger.handlers.clear()

# Docker Compose mounts ./logs to /logs.
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(JsonFormatter())
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())
logger.addHandler(console_handler)
logger.propagate = False

FEATURE_NEW_DASHBOARD = os.getenv("FEATURE_NEW_DASHBOARD", "false").lower() == "true"

@app.route("/")
def home():
    logger.info("Home page accessed; feature_new_dashboard=%s", FEATURE_NEW_DASHBOARD)
    page = "New dashboard feature is ENABLED" if FEATURE_NEW_DASHBOARD else "Classic dashboard"
    return render_template_string("""
      <html><head><title>Lab 3 DevSecOps</title></head>
      <body><h1>Monitoring, Logging & DevSecOps</h1>
      <p id="dashboard">{{ page }}</p>
      <a href="/health">Health check</a></body></html>
    """, page=page)

@app.route("/health")
def health():
    logger.info("Health endpoint called")
    return jsonify(status="healthy", feature_new_dashboard=FEATURE_NEW_DASHBOARD)

@app.route("/simulate-error")
def simulate_error():
    logger.error("Simulated application error for logging demonstration")
    return jsonify(status="error", message="This is a demonstration error"), 500

@app.route("/slow")
def slow():
    time.sleep(0.2)
    logger.info("Slow endpoint requested")
    return jsonify(status="ok", delay_seconds=0.2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
