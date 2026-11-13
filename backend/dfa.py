
# P16 - Airport Ground Incident Logger
# BCS503 - Aircraft Registration DFA

def validate_aircraft_dfa(registration):

    state = "q0"

    for char in registration:

        if state == "q0":
            if char == "V":
                state = "q1"
            else:
                return False

        elif state == "q1":
            if char == "T":
                state = "q2"
            else:
                return False

        elif state == "q2":
            if char == "-":
                state = "q3"
            else:
                return False

        elif state == "q3":
            if char.isascii() and char.isalpha() and char.isupper():
                state = "q4"
            else:
                return False

        elif state == "q4":
            if char.isascii() and char.isalpha() and char.isupper():
                state = "q5"
            else:
                return False

        elif state == "q5":
            if char.isascii() and char.isalpha() and char.isupper():
                state = "q6"
            else:
                return False

        elif state == "q6":
            return False

    return state == "q6"


# DFA Testing
if __name__ == "__main__":

    test_cases = [
        "VT-ABC",
        "VT-XYZ",
        "VT-IND",
        "VT-AB",
        "VT-ABCD",
        "VT-123",
        "vt-abc",
        "VT-A1C",
        "VT-ABC "
    ]

    print("\nAIRCRAFT REGISTRATION DFA")
    print("=" * 40)

    for value in test_cases:
        result = validate_aircraft_dfa(value)

        print(f"{value:10} -> {'ACCEPTED' if result else 'REJECTED'}")
