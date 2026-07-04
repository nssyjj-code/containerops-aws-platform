from flask import Flask, jsonify
import os
import time
import socket

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "containerops-api",
        "version": APP_VERSION
    }), 200


@app.route("/version")
def version():
    return jsonify({
        "version": APP_VERSION,
        "environment": ENVIRONMENT
    }), 200


@app.route("/api/status")
def status():
    return jsonify({
        "service": "containerops-api",
        "status": "running",
        "hostname": socket.gethostname(),
        "environment": ENVIRONMENT,
        "timestamp": int(time.time())
    }), 200


@app.route("/api/error")
def error():
    app.logger.error("Intentional test error triggered")
    return jsonify({
        "status": "error",
        "message": "Intentional test error for monitoring validation"
    }), 500


@app.route("/api/stress-cpu")
def stress_cpu():
    end_time = time.time() + 10
    while time.time() < end_time:
        pass

    return jsonify({
        "status": "completed",
        "message": "CPU stress test completed"
    }), 200


@app.route("/api/stress-memory")
def stress_memory():
    data = ["x" * 1024 * 1024 for _ in range(50)]

    return jsonify({
        "status": "completed",
        "message": "Memory stress test completed",
        "allocated_mb": len(data)
    }), 200


@app.route("/")
def root():
    return jsonify({
        "message": "ContainerOps API is running",
        "docs": [
            "/health",
            "/version",
            "/api/status",
            "/api/error",
            "/api/stress-cpu",
            "/api/stress-memory"
        ]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)