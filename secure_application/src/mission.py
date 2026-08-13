import time


def upload_waypoints(drone):
    print("\n========== UPLOAD WAYPOINTS ==========")

    try:
        count = int(input("Enter number of waypoints: "))

        if count <= 0:
            print("Number of waypoints must be greater than 0.")
            return

        for i in range(count):
            print(f"\nWaypoint {i + 1}")

            latitude = float(input("Latitude: "))
            longitude = float(input("Longitude: "))
            altitude = float(input("Altitude (m): "))

            drone.add_waypoint(latitude, longitude, altitude)

        print("\nWaypoints uploaded successfully.")

    except ValueError:
        print("Invalid input. Please enter numeric values.")


def execute_mission(drone):
    print("\n========== MISSION EXECUTION ==========")

    if not drone.waypoints:
        print("No waypoints available. Upload a mission first.")
        return

    if drone.status == "IN FLIGHT":
        print("Drone is already in flight.")
        return

    print("Starting mission...")
    drone.status = "IN FLIGHT"
    drone.flight_mode = "AUTO"
    drone.speed = 15

    print("Drone status: TAKEOFF")
    drone.altitude = 20

    for index, waypoint in enumerate(drone.waypoints, start=1):
        print(f"\n[{index}/{len(drone.waypoints)}] Flying to waypoint...")

        drone.latitude = waypoint["latitude"]
        drone.longitude = waypoint["longitude"]
        drone.altitude = waypoint["altitude"]

        if drone.battery > 5:
            drone.battery -= 5

        time.sleep(1)

        print(f"[{index}/{len(drone.waypoints)}] Waypoint reached.")

    print("\nReturning to home...")
    time.sleep(1)

    drone.latitude = 28.6139
    drone.longitude = 77.2090
    drone.altitude = 0
    drone.speed = 0
    drone.status = "LANDED"
    drone.flight_mode = "MANUAL"

    print("Mission completed successfully.")