
# P16 - Airport Ground Incident Logger
# BCS503 - Incident Code DFA

def validate_incident_dfa(code):

    state = "q0"

    for char in code:

        if state == "q0":
            if char == "G":
                state = "q1"
            else:
                return False

        elif state == "q1":
            if char == "N":
                state = "q2"
            else:
                return False

        elif state == "q2":
            if char == "D":
                state = "q3"
            else:
                return False

        elif state == "q3":
            if char in "0123456789":
                state = "q4"
            else:
                return False

        elif state == "q4":
            if char in "0123456789":
                state = "q5"
            else:
                return False

        elif state == "q5":
            if char in "0123456789":
                state = "q6"
            else:
                return False

        elif state == "q6":
            return False

    return state == "q6"


# Test cases
if __name__ == "__main__":

    test_cases = [
        "GND123",
        "GND456",
        "GND000",
        "GND12",
        "GND1234",
        "GNDABC",
        "gnd123",
        "GND12A",
        "GND 123"
    ]

    print("\nINCIDENT CODE DFA")
    print("=" * 40)

    for code in test_cases:

        result = validate_incident_dfa(code)

        print(
            f"{code:10} -> "
            f"{'ACCEPTED' if result else 'REJECTED'}"
        )
