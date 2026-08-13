from datetime import datetime
import os

LOG_DIRECTORY = "outputs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "drone_control.log")


def log_event(message):
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def display_logs():
    print("\n========== SYSTEM LOGS ==========")

    if not os.path.exists(LOG_FILE):
        print("No logs available.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        content = file.read()

    if not content:
        print("No logs available.")
        return

    print(content)
