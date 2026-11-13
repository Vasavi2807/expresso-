
import sqlite3
from datetime import datetime

DATABASE = "../database/airport_incidents.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        report_id TEXT PRIMARY KEY,
        reporter_name TEXT,
        aircraft_registration TEXT NOT NULL,
        incident_code TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT,
        priority INTEGER,
        zone TEXT,
        validation_status TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS handlers (
        handler_id INTEGER PRIMARY KEY AUTOINCREMENT,
        handler_name TEXT NOT NULL,
        team TEXT NOT NULL,
        available INTEGER DEFAULT 1,
        capacity INTEGER DEFAULT 5,
        assigned_count INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT,
        handler_id INTEGER,
        team TEXT,
        priority INTEGER,
        backup_used INTEGER DEFAULT 0,
        assigned_at TEXT,
        FOREIGN KEY(report_id) REFERENCES reports(report_id),
        FOREIGN KEY(handler_id) REFERENCES handlers(handler_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT,
        old_status TEXT,
        new_status TEXT,
        updated_at TEXT,
        FOREIGN KEY(report_id) REFERENCES reports(report_id)
    )
    """)

    conn.commit()
    conn.close()

    print("Database and all four tables created successfully!")


def save_report(report):

    conn = get_connection()

    conn.execute("""
    INSERT INTO reports (
        report_id, reporter_name, aircraft_registration,
        incident_code, description, category, priority,
        zone, validation_status, status, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report["report_id"],
        report.get("reporter_name", "Airport Staff"),
        report["aircraft_registration"],
        report["incident_code"],
        report["description"],
        report.get("category"),
        report.get("priority"),
        report.get("zone"),
        report.get("validation_status", "Accepted"),
        report.get("status", "Pending"),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_all_reports():

    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM reports ORDER BY created_at DESC"
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]


def update_report_status(report_id, new_status):

    allowed = ["Pending", "Assigned", "In Progress", "Resolved"]

    if new_status not in allowed:
        raise ValueError("Invalid report status")

    conn = get_connection()

    report = conn.execute(
        "SELECT status FROM reports WHERE report_id = ?",
        (report_id,)
    ).fetchone()

    if report is None:
        conn.close()
        raise ValueError("Report not found")

    old_status = report["status"]

    conn.execute(
        "UPDATE reports SET status = ? WHERE report_id = ?",
        (new_status, report_id)
    )

    conn.execute("""
    INSERT INTO status_history
    (report_id, old_status, new_status, updated_at)
    VALUES (?, ?, ?, ?)
    """, (
        report_id, old_status, new_status,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
