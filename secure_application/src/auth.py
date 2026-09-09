# Simple authentication module.
# This is intentionally kept simple so the project is easy to understand.


USERS = {
    "admin": "admin123",
    "operator": "drone123"
}


def login():
    print("\n========== LOGIN ==========")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in USERS and USERS[username] == password:
        print("\nLogin successful!")
        print(f"Welcome, {username}.")
        return True

    print("\nInvalid username or password.")
    return False(venv)
