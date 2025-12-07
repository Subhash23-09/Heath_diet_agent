from flask import Flask, request, jsonify
from healthbackend.services.orchestrator import orchestrate
from healthbackend.services.auth import require_api_key
from healthbackend.utils.exceptions import InputError, AgentError

app = Flask(__name__)





@app.route("/health-assist", methods=["POST"])
@require_api_key
def health_assist():
    data = request.get_json() or {}
    symptoms = data.get("symptoms")
    medical_report = data.get("medical_report", "")
    user_id = data.get("user_id", "anonymous")

    if not symptoms:
        raise InputError("symptoms is required")

    import asyncio
    # run async orchestrator
    result = asyncio.run(orchestrate(symptoms, medical_report, user_id))
    return jsonify(result)


@app.errorhandler(InputError)
def handle_input_error(err: InputError):
    # bad request from client
    return jsonify({"error": str(err)}), 400


@app.errorhandler(AgentError)
def handle_agent_error(err: AgentError):
    # internal failure from agents / LLM
    return jsonify({"error": "Internal agent failure", "details": str(err)}), 500


def main():
    # debug=True so Flask prints full tracebacks in console
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
