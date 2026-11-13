
# P16 - Airport Ground Incident Logger
# BCS503 - Regex Validation and DFA Comparison

import re

from dfa import validate_aircraft_dfa
from incident_dfa import validate_incident_dfa


# Regular expressions
AIRCRAFT_PATTERN = r"^VT-[A-Z]{3}$"
INCIDENT_PATTERN = r"^GND[0-9]{3}$"


# Regex validation functions
def validate_aircraft_regex(registration):
    return re.fullmatch(AIRCRAFT_PATTERN, registration) is not None


def validate_incident_regex(code):
    return re.fullmatch(INCIDENT_PATTERN, code) is not None


# Compare DFA and Regex results
def compare_validations():

    aircraft_tests = [
        "VT-ABC",
        "VT-XYZ",
        "VT-AB",
        "VT-ABCD",
        "VT-123",
        "vt-abc",
        "VT-A1C"
    ]

    incident_tests = [
        "GND123",
        "GND456",
        "GND12",
        "GND1234",
        "GNDABC",
        "gnd123",
        "GND12A"
    ]

    print("\nAIRCRAFT REGISTRATION COMPARISON")
    print("=" * 75)

    for value in aircraft_tests:

        dfa_result = validate_aircraft_dfa(value)
        regex_result = validate_aircraft_regex(value)

        agreement = dfa_result == regex_result

        print(
            f"{value:12} | "
            f"DFA: {str(dfa_result):5} | "
            f"Regex: {str(regex_result):5} | "
            f"Agreement: {agreement}"
        )

    print("\nINCIDENT CODE COMPARISON")
    print("=" * 75)

    for value in incident_tests:

        dfa_result = validate_incident_dfa(value)
        regex_result = validate_incident_regex(value)

        agreement = dfa_result == regex_result

        print(
            f"{value:12} | "
            f"DFA: {str(dfa_result):5} | "
            f"Regex: {str(regex_result):5} | "
            f"Agreement: {agreement}"
        )


if __name__ == "__main__":
    compare_validations()
