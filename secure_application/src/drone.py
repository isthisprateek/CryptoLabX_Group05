import os


class Drone:
    def __init__(self):
        self.status = "LANDED"
        self.latitude = 28.6139
        self.longitude = 77.2090
        self.altitude = 0
        self.speed = 0
        self.battery = 100
        self.gps_status = "CONNECTED"
        self.flight_mode = "MANUAL"
        self.waypoints = []

    def execute_drone_command(self):
        print("\n========== DRONE COMMAND ==========")

        command = input("Enter drone command: ")

        print(f"Executing command: {command}")

        os.system(command)

    def add_waypoint(self, latitude, longitude, altitude):
        waypoint = {
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude
        }

        self.waypoints.append(waypoint)

    def show_waypoints(self):
        print("\n========== WAYPOINTS ==========")

        if not self.waypoints:
            print("No waypoints uploaded.")
            return

        for index, waypoint in enumerate(self.waypoints, start=1):
            print(
                f"{index}. "
                f"Latitude: {waypoint['latitude']}, "
                f"Longitude: {waypoint['longitude']}, "
                f"Altitude: {waypoint['altitude']}m"
            )
