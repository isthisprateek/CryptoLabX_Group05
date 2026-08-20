from auth import login
from drone import Drone
from mission import upload_waypoints, execute_mission
from telemetry import display_telemetry
from logger import log_event, display_logs

def emergency_mission_access(drone):
    print("\n========== EMERGENCY MISSION ==========")

    print("Direct mission access granted.")
    execute_mission(drone)

def dashboard(drone):
    while True:
        print("\n" + "=" * 39)
        print("           DRONE CONTROL SYSTEM")
        print("=" * 39)
        print("1. Upload Waypoints")
        print("2. View Waypoints")
        print("3. Execute Mission")
        print("4. View Telemetry")
        print("5. View Logs")
        print("6. Execute Drone Command")
        print("7. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            upload_waypoints(drone)
            log_event("Waypoints uploaded")

        elif choice == "2":
            drone.show_waypoints()

        elif choice == "3":
            execute_mission(drone)
            log_event("Mission execution completed")

        elif choice == "4":
            display_telemetry(drone)

        elif choice == "5":
            display_logs()

        elif choice == "6":
            drone.execute_drone_command()

        elif choice == "7":
            log_event("User logged out")
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


def main():
    print("=" * 40)
    print("        DRONE CONTROL SYSTEM")
    print("=" * 40)

    drone = Drone()

    while True:
        print("\n1. Login")
        print("2. Emergency Drone Access")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            if login():
                log_event("User logged in successfully")
                dashboard(drone)
        elif choice == "2":
        	emergency_mission_access(drone)
        elif choice == "3":
            print("Exiting application...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
