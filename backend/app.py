from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "Airport Ground Incident Logger Backend",
        "status": "Running"
    })

@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "Flask API is working!",
        "project": "Airport Ground Incident Logger"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4

from validation_pipeline import validate_report
from routing import dispatch_report
from database import (
    initialize_database,
    save_report,
    get_all_reports,
    update_report_status
)

app = Flask(__name__)
CORS(app)

# Initialize SQLite database
initialize_database()


@app.route("/")
def home():
    return jsonify({
        "message": "Airport Ground Incident Logger",
        "status": "Running"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "message": "Backend connected successfully"
    })


# Submit, validate, classify, route and save a report
@app.route("/api/reports", methods=["POST"])
def submit_report():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "A valid JSON report is required."
        }), 400

    # Step 1: Validate and classify
    result = validate_report(data)

    if not result["success"]:
        return jsonify(result), 400

    # Step 2: Generate report ID
    report_id = "AGI-" + uuid4().hex[:8].upper()

    # Step 3: Prepare dispatch information
    dispatch_data = {
        **data,
        **result,
        "report_id": report_id,
        "validation_status": "Accepted"
    }

    # Step 4: Route the report
    try:
        dispatch_result = dispatch_report(dispatch_data)
    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Dispatch failed: " + str(error)
        }), 500

    # Step 5: Save report in SQLite
    status = dispatch_result.get("status", "Pending")

    if not dispatch_result.get("success"):
        status = dispatch_result.get("status", "Pending")

    stored_report = {
        **dispatch_data,
        "priority": dispatch_result.get("priority"),
        "status": status,
        "zone": data.get("zone")
    }

    try:
        save_report(stored_report)
    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Database save failed: " + str(error)
        }), 500

    return jsonify({
        "success": True,
        "message": "Report processed and saved successfully",
        "report": stored_report,
        "dispatch": dispatch_result
    }), 201


# Get all reports
@app.route("/api/reports", methods=["GET"])
def list_reports():
    return jsonify({
        "success": True,
        "reports": get_all_reports()
    })


# Update report status
@app.route("/api/reports/<report_id>/status", methods=["PATCH"])
def change_status(report_id):

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")

    try:
        update_report_status(report_id, new_status)

        return jsonify({
            "success": True,
            "message": "Report status updated",
            "report_id": report_id,
            "status": new_status
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
