# Drone Control System

A small Python console application that simulates a drone control system.

## Core functionalities

1. Drone login/authentication
2. Waypoint upload
3. Mission execution
4. Telemetry display
5. Log storage

## Project structure

```text
drone_control_system/
│
├── main.py
├── authentication.py
├── drone.py
├── mission.py
├── telemetry.py
├── logger.py
├── README.md
└── outputs/
```

The `outputs` directory is created automatically when the first log is written.

## How to run

Make sure Python 3 is installed.

Run:

```bash
python3 main.py
```

## Demo credentials

Username:
`admin`

Password:
`admin123`

Another account:

Username:
`operator`

Password:
`drone123`

## Important

This project is only a simulation. It does not communicate with or control a real drone.

The security vulnerabilities required by the assignment have NOT been intentionally added yet. First understand the normal functionality. Then the vulnerable versions and fixes can be implemented separately for the security/SAST part of the assignment.