# ShadowTEAM-sys-monitor
these are the same program for system monitoring for three different devices and OS's

# System Monitoring Tool

## Overview

The System Monitoring Tool is a Python script designed to provide real-time monitoring of various system metrics, including CPU usage, RAM usage, storage information, network activity, and GPU temperature and usage. This tool is adaptable for different platforms, supporting Linux (including Raspberry Pi) and Windows operating systems.

### Features

- Live display of CPU usage for each core
- Real-time RAM usage information
- Monitoring of GPU temperature and usage (available for Linux and Windows)
- Storage usage details, including total, used, and free space
- Network activity statistics, showcasing data sent and received
- Active user information
- Adaptable for Linux (including Raspberry Pi) and Windows systems

## Supported Platforms

- Linux (including Raspberry Pi)
- Windows

## Prerequisites

To run the System Monitoring Tool, you'll need the following Python libraries:

### Windows

- `os`: Provides a way of interacting with the operating system.
- `psutil`: A cross-platform library for accessing system details and managing processes.
- `rich`: A library for adding rich terminal text and styling.
- `wmi`: Windows Management Instrumentation, providing access to system resources.
- `time`: Standard Python time-related functions.
- `OpenHardwareMonitor`: This is Software you will have to download in order to get device Temps.
- https://openhardwaremonitor.org/downloads/

### Linux and Raspberry Pi

- `os`: Provides a way of interacting with the operating system.
- `psutil`: A cross-platform library for accessing system details and managing processes.
- `rich`: A library for adding rich terminal text and styling.
- `time`: Standard Python time-related functions.

## Usage

1. Clone the repository.

2. Navigate to the project directory.

3. Run the script:

   For Linux:
python3 Server-Monitor-Linux.py

   For Raspberry Pi:
python3 Server-Monitor-Pi.py

   For Windows:
python3 Server-Monitor-Windows.py


## Configuration

Modify the script variables to suit your preferences or system requirements.

## Troubleshooting

If you encounter issues or errors, refer to the following troubleshooting steps:

1. **GPU Information (Linux):** Ensure that the necessary GPU information commands are available on your Linux system. Adjust the script accordingly if needed.

2. **GPU Information (Windows):** Make sure that the NVIDIA System Management Interface (nvidia-smi) is installed and available in the system's PATH.

3. **Network Attached Drives (Windows):** Ensure that the required permissions are granted for accessing network drives.

## Benefits of Terminal-Only Execution

The System Monitoring Tool runs purely in the terminal, offering the following benefits:

1. **Efficiency:** Operating exclusively in the terminal reduces resource overhead, ensuring efficient monitoring without additional graphical interfaces.

2. **Script Integration:** The terminal-only approach allows easy integration into scripts or automated workflows, enabling seamless inclusion in larger system management processes.

3. **Server Environments:** Ideal for server environments or headless systems where graphical interfaces may not be available or necessary.

## Author

Shadowdrums

