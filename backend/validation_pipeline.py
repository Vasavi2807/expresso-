
# P16 - Airport Ground Incident Logger
# Requirement 4 - Validation and Edge Cases

from dfa import validate_aircraft_dfa
from incident_dfa import validate_incident_dfa
from regex_validation import (
    validate_aircraft_regex,
    validate_incident_regex
)
from classification import classify_incident


def validate_report(report):

    # Check required fields
    required_fields = [
        "aircraft_registration",
        "incident_code",
        "description"
    ]

    for field in required_fields:
        value = report.get(field)

        if not isinstance(value, str) or not value.strip():
            return {
                "success": False,
                "message": f"Missing or invalid field: {field}",
                "validation_status": "Rejected",
                "category": None
            }

    registration = report["aircraft_registration"].strip()
    code = report["incident_code"].strip()
    description = report["description"].strip()

    # DFA and Regex validation
    aircraft_dfa = validate_aircraft_dfa(registration)
    aircraft_regex = validate_aircraft_regex(registration)

    incident_dfa = validate_incident_dfa(code)
    incident_regex = validate_incident_regex(code)

    # Check agreement
    if aircraft_dfa != aircraft_regex:
        return {
            "success": False,
            "message": "Aircraft DFA and Regex disagreement.",
            "validation_status": "Rejected",
            "category": None
        }

    if incident_dfa != incident_regex:
        return {
            "success": False,
            "message": "Incident DFA and Regex disagreement.",
            "validation_status": "Rejected",
            "category": None
        }

    # Reject invalid identifiers
    if not aircraft_dfa:
        return {
            "success": False,
            "message": "Invalid aircraft registration. Expected VT-ABC.",
            "validation_status": "Rejected",
            "category": None
        }

    if not incident_dfa:
        return {
            "success": False,
            "message": "Invalid incident code. Expected GND followed by 3 digits.",
            "validation_status": "Rejected",
            "category": None
        }

    # Classify the incident
    classification = classify_incident(description)

    if not classification["success"]:
        return {
            "success": False,
            "message": classification["message"],
            "validation_status": "Needs Review",
            "category": None
        }

    # Store validation outcome with original report
    return {
        "success": True,
        "validation_status": "Accepted",
        "aircraft_registration": registration,
        "incident_code": code,
        "description": description,
        "category": classification["category"],
        "matched_categories": classification["matched_categories"],
        "matched_keywords": classification["matched_keywords"],
        "message": "Report validated and classified successfully."
    }


# Edge case testing
if __name__ == "__main__":

    test_reports = [

        {
            "aircraft_registration": "VT-ABC",
            "incident_code": "GND123",
            "description": "Metal debris found on runway"
        },

        {
            "aircraft_registration": "VT-AB",
            "incident_code": "GND123",
            "description": "Metal debris found on runway"
        },

        {
            "aircraft_registration": "VT-ABC",
            "incident_code": "GND12",
            "description": "Aircraft damaged"
        },

        {
            "aircraft_registration": "",
            "incident_code": "GND123",
            "description": "Fire reported"
        },

        {
            "aircraft_registration": "VT-ABC",
            "incident_code": "GND123",
            "description": "Unknown issue reported"
        },

        {
            "aircraft_registration": "VT-ABC",
            "incident_code": "GND123",
            "description": "Damaged conveyor caused flight delay"
        }
    ]

    print("\nREPORT VALIDATION AND EDGE CASES")
    print("=" * 60)

    for i, report in enumerate(test_reports, 1):

        result = validate_report(report)

        print(f"\nTEST CASE {i}")
        print("Report:", report)
        print("Status:", result["validation_status"])
        print("Category:", result["category"])
        print("Message:", result["message"])
