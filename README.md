# AlarmCLI ⏰

A lightweight, drift-free, synchronous command-line alarm clock and timer built exclusively with the **Python Standard Library** (zero external dependencies).

---

## ✨ Features

- **Zero External Dependencies**: Runs on standard Python 3.7+ without needing `pip install`.
- **Flexible Time Input**:
  - **Relative Durations**: Supports seconds, minutes, and hours (e.g., `10s`, `5m`, `2h`, `1h 30m`).
  - **Absolute 24-Hour Time**: Supports clock times (e.g., `14:30`, `08:00:00`).
- **Automatic Next-Day Rollover**: If an absolute time is set in the past for today, it automatically schedules for tomorrow.
- **Drift-Free In-Place Countdown**: Computes remaining time dynamically on every tick against system time.
- **CPU Efficient**: Uses adaptive sleeping to prevent CPU pegging while maintaining responsiveness.
- **Audible & Visual Alert**: Beeps on trigger (`winsound` on Windows, ASCII terminal bell `\a` fallback) with an alert banner.
- **Graceful Termination**: Handles `Ctrl+C` cleanly without Python stack traces.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or newer installed.

### Running the Alarm

#### 1. Via Command-Line Arguments

**Relative Timers:**
```bash
# 30-second timer
python alarm.py 30s

# 5-minute timer
python alarm.py 5m

# Combined hours and minutes
python alarm.py "1h 30m"
```

**Absolute 24-Hour Clock Alarms:**
```bash
# Set alarm for 2:30 PM today (or tomorrow if already passed)
python alarm.py 14:30

# Set alarm with seconds precision
python alarm.py 18:45:00
```

#### 2. Interactive Mode

Run without arguments to enter the prompt:
```bash
python alarm.py
```
```text
Enter alarm time or duration (e.g., '10s', '5m', '14:30'): 10s

[+] Alarm set for: 2026-09-11 12:30:10
[+] Press Ctrl+C at any time to cancel.

[COUNTDOWN] Time remaining: 00:00:07
```

---

## 📐 Architecture & Modules

The tool is organized into four synchronous modules within [`alarm.py`](alarm.py):

| Module | Purpose |
|---|---|
| `parse_target_time(time_str)` | Validates and converts relative tokens or 24-hour timestamps into an absolute `datetime` target. |
| `render_countdown(target)` | Renders in-place terminal countdown (`\r`) using dynamic delta calculation to avoid time drift. |
| `trigger_alarm()` | Rings audible beeps and displays a repeating alert banner until dismissed. |
| `main()` | Handles CLI argument parsing, interactive fallback, and top-level `KeyboardInterrupt` cleanup. |

---

## 🛑 Stopping the Alarm

- **During countdown:** Press `Ctrl+C` to cancel the alarm.
- **While ringing:** Press `Ctrl+C` to dismiss the alert.

