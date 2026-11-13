
from datetime import datetime

# Airline-specific routing configuration
ROUTING_TABLE = {
    "AI": {"team": "Air India Ground Team", "zone": "Zone A"},
    "6E": {"team": "IndiGo Ground Team", "zone": "Zone B"},
    "SG": {"team": "SpiceJet Ground Team", "zone": "Zone C"},
    "UK": {"team": "Vistara Ground Team", "zone": "Zone D"}
}

GENERAL_POOL = {
    "team": "General Handling Team",
    "zone": "Central Zone"
}

SAFETY_OFFICER = "Airport Safety Officer"

PRIORITY = {
    "Safety Breach": 1,
    "Damage": 2,
    "Equipment Failure": 3,
    "FOD": 4,
    "Delay": 5
}

HANDLERS = [
    {"id": "H01", "name": "Handler 1", "team": "Air India Ground Team",
     "available": True, "capacity": 2, "assigned": 0},

    {"id": "H02", "name": "Handler 2", "team": "IndiGo Ground Team",
     "available": True, "capacity": 2, "assigned": 0},

    {"id": "H03", "name": "Handler 3", "team": "SpiceJet Ground Team",
     "available": True, "capacity": 2, "assigned": 0},

    {"id": "H04", "name": "Handler 4", "team": "Vistara Ground Team",
     "available": True, "capacity": 2, "assigned": 0},

    {"id": "H05", "name": "General Handler", "team": "General Handling Team",
     "available": True, "capacity": 5, "assigned": 0}
]

# Prevent duplicate assignments during runtime
PROCESSED_REPORTS = set()


def dispatch_report(report):

    report_id = report.get("report_id")
    registration = report.get("aircraft_registration", "")
    category = report.get("category")
    zone_input = report.get("zone", "")

    if not report_id or not registration.startswith("VT-") or category not in PRIORITY:
        return {"success": False, "message": "Invalid report or routing data."}

    if report_id in PROCESSED_REPORTS:
        return {"success": False, "message": "Duplicate assignment prevented."}

    carrier_code = report.get("carrier_code", "").upper()

    route = ROUTING_TABLE.get(carrier_code)

    if route:
        team = route["team"]
        zone = zone_input or route["zone"]
    else:
        team = GENERAL_POOL["team"]
        zone = zone_input or GENERAL_POOL["zone"]

    # Emergency priority override
    priority = PRIORITY[category]
    emergency = category == "Safety Breach"

    if emergency:
        priority = 0

    eligible = [
        h for h in HANDLERS
        if h["team"] == team
        and h["available"]
        and h["assigned"] < h["capacity"]
    ]

    # Backup to general pool if airline team is unavailable
    backup_used = False

    if not eligible and team != GENERAL_POOL["team"]:
        eligible = [
            h for h in HANDLERS
            if h["team"] == GENERAL_POOL["team"]
            and h["available"]
            and h["assigned"] < h["capacity"]
        ]
        backup_used = True

    if not eligible:
        return {
            "success": True,
            "report_id": report_id,
            "status": "Pending",
            "priority": priority,
            "message": "No handler available. Report placed in waiting queue.",
            "queue_priority": priority
        }

    handler = min(eligible, key=lambda h: h["assigned"])

    handler["assigned"] += 1
    PROCESSED_REPORTS.add(report_id)

    return {
        "success": True,
        "report_id": report_id,
        "zone": zone,
        "team": handler["team"],
        "handler_id": handler["id"],
        "handler_name": handler["name"],
        "priority": priority,
        "status": "Assigned",
        "backup_used": backup_used,
        "safety_notification": SAFETY_OFFICER if emergency else None,
        "assigned_at": datetime.now().isoformat(),
        "message": "Report successfully dispatched."
    }


if __name__ == "__main__":

    sample = {
        "report_id": "R001",
        "aircraft_registration": "VT-ABC",
        "carrier_code": "AI",
        "category": "Safety Breach",
        "zone": "Zone A"
    }

    print(dispatch_report(sample))
