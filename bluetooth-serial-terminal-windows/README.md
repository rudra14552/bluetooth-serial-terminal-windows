# Bluetooth Serial Terminal for Windows

A desktop application for Windows that connects to Bluetooth devices (like HC-05 modules) and allows you to send/receive serial UART data over Bluetooth.

## Features

- 🔍 **Device Discovery**: Scan and list available Bluetooth devices
- 📝 **Device History**: Automatically remembers last connected port and baud rate with timestamps
- 💬 **Chat Interface**: Interactive terminal for sending and receiving data with message numbering
- ⚙️ **Baud Rate Selection**: Support for common baud rates (9600, 19200, 38400, 57600, 115200)
- 📡 **Real-time Communication**: Send and receive serial data over Bluetooth
- 🔄 **Auto-reconnect**: Automatically reconnects to last used port on startup
- 🧹 **Buffer Management**: Automatic buffer clearing on connect + manual clear button
- 📊 **Message Tracking**: Shows TX/RX direction, message numbers, and byte counts
- 🗑️ **Clear Chat**: Clear the display while keeping the connection active

## Installation on Windows

### Prerequisites
1. **Pair your Bluetooth device** in Windows Settings first:
   - Settings → Devices → Bluetooth & other devices
   - Turn on Bluetooth
   - Add Bluetooth or other device → Bluetooth
   - Select your device (HC-05, HC-06, etc.) and pair it
   - Windows will create a virtual COM port for the device

### Method 1: Using Python (Recommended)

1. **Install Python 3.11+** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Download this project** files to your computer

3. **Install dependencies**:
   - Open Command Prompt in the project folder
   - Run: `pip install pyserial`

4. **Run the application**:
   ```
   python main.py
   ```

### Method 2: Using the Batch File

1. Double-click `run.bat` (Windows will install dependencies and start the app)

## How to Use

1. **Pair Device First**: Pair your Bluetooth device in Windows Settings (see Prerequisites)
2. **Refresh Ports**: Click "Refresh Ports" to scan for available COM ports
3. **Select Port**: Click on the COM port for your Bluetooth device (marked with 📶)
4. **Set Baud Rate**: Choose your desired baud rate from the dropdown (default: 9600)
5. **Connect**: Click "Connect" to establish connection
6. **Send Data**: Type your message and press Enter or click "Send"
7. **Receive Data**: Incoming data appears in green in the chat window

## Device History

The application automatically saves the last connected port to `device_history.json`. The previously used port is auto-selected when you refresh ports, allowing quick reconnection.

## Buffer Management

The app includes smart buffer management to prevent old/stale data from mixing with new data:

- **Auto-Clear on Connect**: Automatically clears input and output buffers when connecting
- **Manual Clear**: Use the "Clear Buffers" button to manually flush buffers during operation
- **Message Tracking**: Each message shows:
  - 📤 TX (Transmit) or 📥 RX (Receive) indicator
  - Message number (#1, #2, #3...)
  - Byte count for each message
  - Actual data sent/received
- **Clear Chat**: Clear the display without disconnecting (keeps connection active)

## Supported Devices

- HC-05 Bluetooth modules
- HC-06 Bluetooth modules
- Arduino with Bluetooth
- ESP32 with Bluetooth
- Any Bluetooth device supporting serial communication (SPP profile)

## Troubleshooting

### No COM Ports Found
- Ensure Bluetooth is enabled on your Windows laptop
- Make sure you've paired the device in Windows Settings first
- The device must be paired (not just discovered) to create a COM port
- Check that the device is not connected to another device (phone, etc.)

### Connection Errors
- Verify the device is paired in Windows Settings
- Check that the correct COM port is selected
- Try disconnecting the device from other devices first
- Some devices may need to be in specific modes

### Can't Send/Receive Data
- Ensure the device is properly connected (status shows "Connected")
- Check that the baud rate matches your device's configuration (common: 9600 for HC-05/06)
- Try different line ending options (None, \n, \r, \r\n)
- Verify the device is powered on and in range

### How to Find Device COM Port
1. Open Device Manager in Windows
2. Expand "Ports (COM & LPT)"
3. Look for your Bluetooth device with a COM port number
4. Use that COM port in the application

## Technical Details

- **Language**: Python 3.11+
- **GUI Framework**: Tkinter (built-in)
- **Serial Communication**: PySerial
- **Platform**: Windows (uses COM ports created by Bluetooth pairing)

## License

Free to use and modify for personal and commercial projects.
