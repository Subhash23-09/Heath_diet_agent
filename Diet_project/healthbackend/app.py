import asyncio
from flask import Flask, request, jsonify

from healthbackend.services.orchestrator import orchestrate
from healthbackend.services.history_store import get_history
from healthbackend.services.auth import require_api_key

from healthbackend.utils.exceptions import AuthError, InputError, AgentError

app = Flask(__name__)

# -------------------------
# Error Handlers
# -------------------------
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({"error": str(e)}), 401

@app.errorhandler(InputError)
def input_error(e):
    return jsonify({"error": str(e)}), 400

#@app.errorhandler(AgentError)
#def agent_error(e):
#    return jsonify({"error": "Internal agent failure"}), 500


# -------------------------
# Health Assist API
# -------------------------
@app.route("/health-assist", methods=["POST"])
@require_api_key
def health_assist():
    data = request.get_json()

    if not data or "symptoms" not in data:
        raise InputError("Symptoms required")

    #  Bridge async agents safely inside sync Flask
    result = asyncio.run(
        orchestrate(
            data["symptoms"],
            data.get("medical_report"),
            data.get("user_id", "guest")
        )
    )

    return jsonify(result)


# -------------------------
# History API
# -------------------------
@app.route("/history/<user_id>")
@require_api_key
def history(user_id):
    return jsonify({
        "user_id": user_id,
        "history": get_history(user_id)
    })

@app.route("/", methods=["GET"])
def welcome_health():
    return "Welcome to Health & Diet Care"

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
