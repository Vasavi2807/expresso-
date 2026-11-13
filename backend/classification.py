
# P16 - Airport Ground Incident Logger
# BCS503 - Incident Classification

import re


# Five predefined incident categories and their keywords
CATEGORY_KEYWORDS = {
    "Safety Breach": [
        "safety breach",
        "safety violation",
        "unauthorized",
        "restricted area",
        "fire",
        "smoke",
        "fuel leak",
        "unsafe",
        "security violation"
    ],

    "Damage": [
        "damage",
        "damaged",
        "collision",
        "crack",
        "dent",
        "scratched",
        "structural damage",
        "broken aircraft"
    ],

    "Equipment Failure": [
        "equipment failure",
        "malfunction",
        "not working",
        "stopped working",
        "out of order",
        "conveyor",
        "belt loader",
        "ground support equipment",
        "gpu failure"
    ],

    "FOD": [
        "foreign object debris",
        "fod",
        "debris",
        "metal object",
        "loose object",
        "bird strike",
        "rubbish"
    ],

    "Delay": [
        "delay",
        "delayed",
        "late departure",
        "departure postponed",
        "schedule disruption"
    ]
}


# Documented deterministic priority rule
CATEGORY_PRIORITY = [
    "Safety Breach",
    "Damage",
    "Equipment Failure",
    "FOD",
    "Delay"
]


def find_matching_keywords(description, keywords):

    matched = []

    for keyword in keywords:

        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

        if re.search(pattern, description, re.IGNORECASE):
            matched.append(keyword)

    return matched


def classify_incident(description):

    if not isinstance(description, str) or not description.strip():
        return {
            "success": False,
            "category": None,
            "matched_categories": [],
            "matched_keywords": [],
            "message": "Incident description cannot be empty."
        }

    all_matches = {}

    # Check all five categories
    for category, keywords in CATEGORY_KEYWORDS.items():

        matches = find_matching_keywords(description, keywords)

        if matches:
            all_matches[category] = matches

    # No matching category found
    if not all_matches:
        return {
            "success": False,
            "category": None,
            "matched_categories": [],
            "matched_keywords": [],
            "message": "Unknown incident. Manual classification required."
        }

    # Apply deterministic priority
    selected_category = next(
        category
        for category in CATEGORY_PRIORITY
        if category in all_matches
    )

    return {
        "success": True,
        "category": selected_category,
        "matched_categories": list(all_matches.keys()),
        "matched_keywords": all_matches[selected_category],
        "message": f"Incident classified as {selected_category}."
    }


# Testing the classification system
if __name__ == "__main__":

    test_cases = [
        "Metal debris found on runway",
        "Aircraft wing damaged during ground handling",
        "Flight delayed due to ground operations",
        "Unauthorized person entered restricted area",
        "Baggage conveyor stopped working",
        "Damaged conveyor caused flight delay",
        "Fire reported near aircraft",
        "Bird strike reported on runway",
        "Unknown issue reported",
        ""
    ]

    print("\nAIRPORT INCIDENT CLASSIFICATION")
    print("=" * 65)

    for description in test_cases:

        result = classify_incident(description)

        print(f"\nIncident: {description}")

        if result["success"]:
            print("Category:", result["category"])
            print("Matched categories:", result["matched_categories"])
            print("Matched keywords:", result["matched_keywords"])
        else:
            print("Category: UNCLASSIFIED")
            print("Message:", result["message"])
