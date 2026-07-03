# Bluetooth Serial Terminal for Windows

## Project Overview
This is a desktop application that provides Bluetooth serial terminal functionality for Windows, similar to the Android app "Serial Bluetooth Terminal". It allows users to connect their Windows laptop's Bluetooth to other Bluetooth devices (like HC-05, HC-06 modules) and send/receive serial UART data.

## Purpose
- Enable Windows users to communicate with Bluetooth serial devices
- Provide a chat-like interface for interactive UART communication
- Remember device history for quick reconnections
- Support configurable baud rates for different devices

## Project Structure
```
.
├── main.py              # Main application with GUI and Bluetooth logic
├── launcher.py          # Environment-aware launcher script
├── run.bat             # Windows batch file for easy launching
├── README.md           # User documentation
├── replit.md           # Project documentation (this file)
└── device_history.json # Auto-generated device connection history
```

## Key Features Implemented
1. **Bluetooth Device Discovery** - Scan and list available Bluetooth devices
2. **Device History** - Automatically saves and displays previously connected devices
3. **Interactive Chat UI** - Send and receive data in a messaging-style interface
4. **Baud Rate Selection** - Support for common rates (9600-115200)
5. **Real-time Communication** - Threaded send/receive over Bluetooth COM ports
6. **Auto-reconnect** - Automatically reconnects to last used port/baud on startup

## Technology Stack
- **Language**: Python 3.11+
- **GUI Framework**: Tkinter (built-in)
- **Serial Communication**: PySerial
- **Threading**: For non-blocking serial I/O

## How It Works
1. User pairs Bluetooth device in Windows Settings (creates virtual COM port)
2. Application scans for available COM ports
3. User selects COM port and baud rate, then connects
4. PySerial opens the COM port with specified settings
5. Background thread continuously reads incoming serial data
6. Data is sent/received through the serial port
7. Chat interface displays all communication with timestamps

## Important Notes for Replit
⚠️ **This application cannot run on Replit** because:
- Requires physical Bluetooth hardware access
- Needs GUI display (DISPLAY environment variable)
- Designed for local Windows installation

The launcher script detects Replit environment and provides download instructions.

## For Users
To use this application:
1. Download all project files to your Windows computer
2. Install Python 3.11+ from python.org
3. Either:
   - Double-click `run.bat`, OR
   - Run `python main.py` in command prompt

## Recent Changes
- 2025-10-12: Initial project creation
  - Implemented full Bluetooth serial terminal
  - Added GUI with tkinter
  - Added device history persistence
  - Created Windows launcher script
  - Added comprehensive documentation

## Architecture Decisions
- **PySerial for COM Ports**: Windows Bluetooth pairing creates virtual COM ports, PySerial provides reliable serial communication
- **Tkinter GUI**: Built-in, no extra dependencies, lightweight
- **Threading**: Background thread for continuous serial reading keeps GUI responsive
- **JSON persistence**: Simple device history storage for last used port
- **SPP Profile**: Uses standard Serial Port Profile compatible with HC-05/06 and similar devices

## Future Enhancements
- Add support for custom baud rates
- Implement data logging to file
- Add hex/ASCII view toggle
- Support for sending files
- Auto-reconnect on disconnect
- Advanced UART settings (parity, stop bits)
