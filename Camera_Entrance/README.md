# Traffic Monitoring Application

This Python application uses the NetSDK to monitor traffic events from a video analytics system. It captures and saves images related to traffic junction events, storing them in organized directories.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [License](#license)

## Features

- Monitors traffic junction events and captures relevant images.
- Saves captured images in separate directories for easy access.
- Provides real-time monitoring with the ability to stop and clean up resources gracefully.

## Requirements

- Python 3.x
- PyQt5
- NetSDK library (ensure you have the necessary SDK files and dependencies)
- Operating system: Windows (as it relies on ctypes for handling the SDK)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Required Packages**:
   Make sure to install PyQt5. You can install it using pip:
   ```bash
   pip install PyQt5
   ```

3. **Set Up NetSDK**:
   Ensure that you have the NetSDK library available. You may need to place the SDK files in the same directory as your script or ensure they are accessible in your Python environment.

## Usage

1. **Configuration**:
   Edit the section in the code where the IP address, port, username, and password are defined:
   ```python
   ip = "10.118.210.122"
   port = 37777
   username = "admin"
   password = "petabyte2024"
   ```

2. **Run the Application**:
   Execute the script:
   ```bash
   python traffic_monitor.py
   ```

3. **Stop the Monitoring**:
   You can stop the monitoring process by pressing `Ctrl + C` in the terminal where the script is running.

## Directory Structure

When the application is run, it will create the following structure in the current working directory:

```
data/
├── Global/
│   └── Global_Img<number>.jpg
└── Small/
    └── Small_Img<number>.jpg
```

- **data/**: Main directory containing images.
- **Global/**: Directory for storing global images captured from traffic events.
- **Small/**: Directory for storing smaller images related to traffic events.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
