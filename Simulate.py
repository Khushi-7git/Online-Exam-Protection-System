"""
Exam Guard Simulator
Simulates exam detection and process termination events WITHOUT
actually killing real system processes. Safe for testing/demo.
"""

import json
import time
import random
import os
from datetime import datetime

EVENT_LOG_FILE = os.path.join(os.path.dirname(__file__), "events.json")

SIMULATED_EXAM_APPS = ["SafeExamBrowser", "Zoom", "Teams"]

SIMULATED_BLACKLISTED = [
    "firefox", "chrome", "discord", "spotify", "vlc",
    "telegram", "steam", "obs", "vscode", "slack"
]

SIMULATED_PROTECTED = [
    {"name": "systemd",       "pid": 1,    "cpu": 0.1,  "mem": 0.2,  "status": "sleeping"},
    {"name": "NetworkManager","pid": 842,  "cpu": 0.0,  "mem": 0.5,  "status": "sleeping"},
    {"name": "pulseaudio",    "pid": 1204, "cpu": 0.2,  "mem": 0.8,  "status": "sleeping"},
    {"name": "gnome-shell",   "pid": 1581, "cpu": 1.4,  "mem": 2.1,  "status": "running"},
    {"name": "Xorg",          "pid": 1003, "cpu": 0.6,  "mem": 1.2,  "status": "running"},
    {"name": "python3",       "pid": os.getpid(), "cpu": 0.3, "mem": 0.9, "status": "running"},
]


def default_data():
    return {
        "exam_mode": False,
        "exam_app": None,
        "start_time": None,
        "events": [],
        "terminated": [],
        "protected": [],
        "stats": {
            "total_terminated": 0,
            "scan_count": 0,
            "uptime_seconds": 0
        }
    }


def load_data():
    if os.path.exists(EVENT_LOG_FILE):
        try:
            with open(EVENT_LOG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return default_data()


def save_data(data):
    with open(EVENT_LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_event(data, level, message, process=None):
    data["events"].insert(0, {
        "time": datetime.now().isoformat(),
        "level": level,
        "message": message,
        "process": process
    })
    data["events"] = data["events"][:100]


def run_simulation():
    print("=" * 58)
    print("  Online Exam Protection System — SIMULATOR MODE")
    print("  (No real processes will be terminated)")
    print("=" * 58)

    data = default_data()
    save_data(data)
    add_event(data, "INFO", "Simulator started. Watching for exam applications...")
    save_data(data)

    scan_count = 0
    start_time = time.time()
    exam_active = False
    chosen_exam_app = None

    # Simulation timeline
    # Phase 1: Idle (5 scans)
    # Phase 2: Exam detected → enforce (8 scans)
    # Phase 3: Exam ends (3 scans)
    # Phase 4: Repeat

    phase = "idle"
    phase_counter = 0

    try:
        while True:
            scan_count += 1
            uptime = int(time.time() - start_time)
            phase_counter += 1

            # Advance phases
            if phase == "idle" and phase_counter >= 5:
                phase = "exam"
                phase_counter = 0
                chosen_exam_app = random.choice(SIMULATED_EXAM_APPS)
                exam_active = True
                data["exam_mode"] = True
                data["exam_app"] = chosen_exam_app
                data["start_time"] = datetime.now().isoformat()
                add_event(data, "CRITICAL",
                          f"Exam Mode ACTIVATED. Detected: {chosen_exam_app}", chosen_exam_app)
                print(f"\n🔴 EXAM MODE ACTIVATED — {chosen_exam_app} detected\n")

            elif phase == "exam" and phase_counter >= 8:
                phase = "ending"
                phase_counter = 0

            elif phase == "ending" and phase_counter >= 3:
                phase = "idle"
                phase_counter = 0
                exam_active = False
                data["exam_mode"] = False
                data["exam_app"] = None
                data["start_time"] = None
                add_event(data, "INFO", "Exam Mode DEACTIVATED. System restored to normal.")
                print(f"\n🟢 EXAM MODE DEACTIVATED — System restored\n")

            # Simulate process termination during exam phase
            if phase == "exam" and random.random() < 0.6:
                victim = random.choice(SIMULATED_BLACKLISTED)
                fake_pid = random.randint(2000, 9999)
                entry = {"name": victim, "pid": fake_pid,
                         "time": datetime.now().isoformat()}
                data["terminated"].insert(0, entry)
                data["terminated"] = data["terminated"][:50]
                data["stats"]["total_terminated"] += 1
                add_event(data, "WARNING",
                          f"Process terminated: {victim} (PID {fake_pid})", victim)
                print(f"  ⚠  Terminated: {victim} (PID {fake_pid})")
            else:
                if exam_active:
                    print(f"  ✓  Scan #{scan_count}: Environment clean.")
                else:
                    print(f"  [IDLE]  Scan #{scan_count}: No exam detected. Monitoring...")

            # Update stats & protected list
            data["stats"]["scan_count"] = scan_count
            data["stats"]["uptime_seconds"] = uptime
            data["protected"] = SIMULATED_PROTECTED

            save_data(data)
            time.sleep(3)

    except KeyboardInterrupt:
        data["exam_mode"] = False
        add_event(data, "INFO", "Simulator stopped by user.")
        save_data(data)
        print("\n\nSimulator stopped.")


if __name__ == "__main__":
    run_simulation()