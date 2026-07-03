# Bluetooth Serial Terminal

A lightweight Windows desktop app for chatting with Bluetooth serial devices (HC-05, HC-06, Arduino, ESP32, etc.) over paired COM ports — like the "Serial Bluetooth Terminal" Android app, but for your PC.

I built this because I often wanted to use a Bluetooth serial terminal from my laptop and couldn't find a decent app for it — so I made one myself, with help from [Replit](https://replit.com).

<img width="1121" height="910" alt="Screenshot 2026-07-03 145553" src="https://github.com/user-attachments/assets/4ddbe5f7-9c97-4b59-ab7f-cfad20d871f0" />


## Features

- 🔍 **Device Discovery** — Scan and list available COM ports (Bluetooth & regular serial)
- 📝 **Device History** — Automatically remembers last connected port and baud rate, with timestamps
- 💬 **Chat Interface** — Interactive terminal for sending and receiving data with message numbering
- ⚙️ **Baud Rate Selection** — Common baud rates (9600, 19200, 38400, 57600, 115200)
- 📡 **Real-time Communication** — Send and receive serial data over Bluetooth
- 🔄 **Auto-reconnect** — Automatically reconnects to the last used port on startup
- 🧹 **Buffer Management** — Automatic buffer clearing on connect + manual clear button
- 📊 **Message Tracking** — Shows TX/RX direction, message numbers, and byte counts
- 🗑️ **Clear Chat** — Clear the display while keeping the connection active

## Installation

### Prerequisites

1. **Install Python 3.11+** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
2. **Download this project** to your computer
3. **Install dependencies**:
   ```
   pip install pyserial
   ```

## Setting Up a Bluetooth COM Port (Do This First)



https://github.com/user-attachments/assets/3e468a87-adb7-4ab6-b0c5-c4a38533dd27



Before the app can talk to your Bluetooth device, Windows needs a virtual COM port for it. This app does **not** create the connection itself — it just talks over a COM port that Windows creates.

1. Open **Settings → Bluetooth & devices → More Bluetooth settings**
2. Go to the **COM Ports** tab
3. Click **Add**
4. Select your device, then choose:
   - **Incoming** — if the *other device* will initiate the connection to your PC
   - **Outgoing** — if your *PC* will initiate the connection to the other device
   - You can also add **both** an incoming and an outgoing port for the same device if you're not sure which side will connect first
   
   > **Note:** Incoming/Outgoing only refers to *which side makes the connection request*. Once connected, data flows both ways (RX and TX) regardless of which type you chose.
5. Click **OK** — Windows will assign a COM port number (e.g. COM9) to the device

## How to Use



https://github.com/user-attachments/assets/7a770d9a-ce07-4de9-9a4e-96354b06e6bd



1. **Set up the COM port** first (see above) if you haven't already
2. **Run the app**:
   - Double-click `run.bat`, OR
   - Run `python main.py` from the command prompt
3. **Select the COM port** for your device from the list
4. **Select the baud rate** matching your device (default: 9600)
5. **Click Connect**

   > **Note:** Connecting the COM port in this app lets you *intercept the serial data* flowing over that port — but you still need to manually connect the actual Bluetooth device to your PC (via Windows Bluetooth settings or the device itself) for any data to actually flow.
6. **Send data**: Type your message and press Enter or click "Send"
7. **Receive data**: Incoming data appears in green in the chat window

## Device History

The app automatically saves the last connected port to `device_history.json`. The previously used port is auto-selected and auto-reconnected when you launch the app, so you can get back to work quickly.

## Buffer Management

- **Auto-Clear on Connect** — Clears input and output buffers automatically when connecting
- **Manual Clear** — "Clear Buffers" button flushes buffers during operation
- **Message Tracking** — Each message shows:
  - 📤 TX (Transmit) or 📥 RX (Receive) indicator
  - Message number (#1, #2, #3...)
  - Byte count for each message
  - Actual data sent/received
- **Clear Chat** — Clears the display without disconnecting

## Supported Devices

- HC-05 / HC-06 Bluetooth modules
- Arduino with Bluetooth
- ESP32 with Bluetooth
- Any Bluetooth device supporting serial communication (SPP profile)

## Note
This isn't a polished, fully-fledged application — it's a personal utility tool I built for my own use, and it's helped me out a lot. Sharing it here in case others find it useful too.

## Troubleshooting

### No COM Ports Found
- Make sure you've added a COM port for the device via **Bluetooth Settings → More Bluetooth settings → COM Ports → Add** (see setup steps above)
- The device must have a COM port assigned — just being paired isn't enough

### Connection Errors
- Double-check the correct COM port is selected
- Make sure no other application (like Arduino IDE's Serial Monitor) has the port open
- Confirm the Bluetooth device itself is actually connected, not just that the COM port is open

### Can't Send/Receive Data
- Confirm the device is connected (status shows "Connected") **and** the actual Bluetooth link is active
- Check that the baud rate matches your device's configuration (commonly 9600 for HC-05/06)
- Try different line ending options (None, \n, \r, \r\n)
- Verify the device is powered on and in range

### How to Find Your Device's COM Port
1. Open **Device Manager** in Windows
2. Expand **Ports (COM & LPT)**
3. Look for your Bluetooth device's COM port number
4. Use that COM port in the app

## Technical Details

- **Language**: Python 3.11+
- **GUI Framework**: Tkinter (built-in)
- **Serial Communication**: PySerial
- **Platform**: Windows (uses COM ports created via Bluetooth pairing)

## License

MIT License — free to use and modify for personal and commercial projects.
