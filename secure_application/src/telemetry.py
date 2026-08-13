def display_telemetry(drone):
    print("\n========== DRONE TELEMETRY ==========")

    print(f"Status       : {drone.status}")
    print(f"Latitude     : {drone.latitude}")
    print(f"Longitude    : {drone.longitude}")
    print(f"Altitude     : {drone.altitude} m")
    print(f"Speed        : {drone.speed} m/s")
    print(f"Battery      : {drone.battery}%")
    print(f"GPS Signal   : {drone.gps_status}")
    print(f"Flight Mode  : {drone.flight_mode}")

    print("=" * 38)
