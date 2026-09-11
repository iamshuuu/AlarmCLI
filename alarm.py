#!/usr/bin/env python3
"""
Python CLI Alarm Clock
Standard Library Only (Zero external dependencies)
"""

import sys
import time
from datetime import datetime, timedelta

# Platform-specific audio beep support (Windows fallback to standard terminal bell)
try:
    import winsound
    def play_beep():
        winsound.Beep(1200, 400)
except ImportError:
    def play_beep():
        sys.stdout.write('\a')
        sys.stdout.flush()


def parse_target_time(time_str: str) -> datetime:
    """
    Parses a 24-hour time string ('HH:MM' or 'HH:MM:SS') and computes
    the absolute target datetime. If the time has already passed today,
    it automatically rolls over to the next day.
    """
    time_str = time_str.strip()
    parsed_time = None

    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            parsed_time = datetime.strptime(time_str, fmt).time()
            break
        except ValueError:
            continue

    if parsed_time is None:
        raise ValueError(f"Invalid time format '{time_str}'. Expected 24-hr format (HH:MM or HH:MM:SS).")

    now = datetime.now()
    target = datetime.combine(now.date(), parsed_time)

    # Roll over to tomorrow if target time is in the past for today
    if target <= now:
        target += timedelta(days=1)

    return target


def render_countdown(target: datetime) -> None:
    """
    Renders a live, drift-free in-place terminal countdown until target time is reached.
    Uses adaptive sleep to avoid CPU pegging and prevent drift.
    """
    print(f"\n[+] Alarm set for: {target.strftime('%Y-%m-%d %H:%M:%S')}")
    print("[+] Press Ctrl+C at any time to cancel.\n")

    while True:
        now = datetime.now()
        diff = target - now
        total_seconds = diff.total_seconds()

        if total_seconds <= 0:
            break

        total_sec_int = int(total_seconds)
        hours, remainder = divmod(total_sec_int, 3600)
        minutes, seconds = divmod(remainder, 60)

        sys.stdout.write(f"\r[COUNTDOWN] Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d} ")
        sys.stdout.flush()

        # Sleep up to 1 second without oversleeping past the target
        time.sleep(min(1.0, max(0.01, total_seconds)))

    # Clear countdown line
    sys.stdout.write("\r" + " " * 50 + "\r")
    sys.stdout.flush()


def trigger_alarm() -> None:
    """
    Triggers visual and audible alerts when the alarm goes off.
    Loops until interrupted by user (Ctrl+C) or after max cycles.
    """
    print("\n" + "=" * 45)
    print("       🔔 ⏰  ALARM RINGING! ⏰ 🔔       ")
    print("       Press Ctrl+C to dismiss alarm     ")
    print("=" * 45 + "\n")

    cycles = 0
    max_cycles = 20  # Ring for ~20 iterations if unattended

    while cycles < max_cycles:
        play_beep()
        time.sleep(0.3)
        cycles += 1

    print("\n[+] Alarm finished.")


def main() -> None:
    """
    Main entry point: coordinates input parsing, countdown, and alarm triggering.
    """
    try:
        if len(sys.argv) > 1:
            time_input = " ".join(sys.argv[1:])
        else:
            time_input = input("Enter alarm time (e.g 14:30 or 5m, 10s):")

        if not time_input.strip():
            print("[!] Error: No time provided.")
            sys.exit(1)

        target = parse_target_time(time_input)
        render_countdown(target)
        trigger_alarm()

    except ValueError as err:
        print(f"[!] Error: {err}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n[INFO] Alarm stopped / cancelled by user. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()

