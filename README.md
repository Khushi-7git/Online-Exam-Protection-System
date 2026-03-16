# Online Exam Protection System

![Screenshot 2026-03-16 223846](https://github.com/user-attachments/assets/49960714-3386-463e-b282-c6befeeae2fd)

---

## Project Overview

This system simulates how an Operating System enforces **priority-based process control** during critical events such as online examinations. When an exam application is running, all non-essential background processes are detected and terminated, ensuring a secure, distraction-free, and fair environment.

---

## Files

| File | Purpose |
|---|---|
| `exam_guard.py` | **Core engine** — Real process monitor, requires sudo on Linux/macOS |
| `simulate.py` | **Safe simulator** — Demonstrates exam cycle without killing real processes |
| `dashboard.html` | **Live dashboard** — Open in browser alongside the simulator |
| `events.json` | Auto-generated data file read by the dashboard |
| `exam_guard.log` | Auto-generated text log |

---

## How to Run

### 1. Install dependencies
```bash
pip install psutil
```

### 2. Run the Simulator (safe, no root needed)
```bash
python3 simulate.py
```
Then open `dashboard.html` in your browser to see the live dashboard.

### 3. Run the Real Guard (Linux/macOS — requires elevated privileges)
```bash
sudo python3 exam_guard.py
```
Add any exam application name to `EXAM_APPLICATIONS` in `exam_guard.py` to detect it.

---

## System Flow

```
Monitor All Processes
        ↓
Is Exam App Running?
    ↓          ↓
   YES          NO
    ↓           ↓
Activate     Stay IDLE
Exam Mode        ↓
    ↓        Continue
Find Blacklisted  Monitoring
Processes
    ↓
Terminate Them
    ↓
Protect Critical
Processes
    ↓
Continue Loop
```

---

## Key Configuration (in exam_guard.py)

| Variable | Purpose |
|---|---|
| `EXAM_APPLICATIONS` | Apps that trigger Exam Mode |
| `BLACKLISTED_APPLICATIONS` | Apps terminated during Exam Mode |
| `PROTECTED_PROCESSES` | Apps never terminated (system + exam) |
| `MONITOR_INTERVAL` | Scan frequency in seconds (default: 3) |

---

## OS Concepts Demonstrated

- **Process Management** — Listing, inspecting, and terminating processes via `psutil`
- **Priority-Based Scheduling** — Protecting high-priority (exam) processes over background ones
- **Inter-Process Communication** — JSON-based event bus between guard and dashboard
- **Signal Handling** — Graceful shutdown on SIGINT/SIGTERM
- **Resource Control** — Freeing CPU and memory by terminating non-essential processes
