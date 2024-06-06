# USB Key Security System

This project provides a security mechanism for Windows computers, allowing access only when a specific USB device is connected. The system requires a PIN for access and checks for the USB device continuously.

## Supported Platforms

- **Only Works On Windows Operating System**

## Features

- **USB Authentication**: The system locks the computer unless a specific USB device is connected.
- **PIN Protection**: A 6-digit PIN is required to unlock the computer when the USB device is connected.
- **System Tray Control**: Pause, continue, and quit the security check from the system tray.
- **Automatic Startup**: Option to run the security system at Windows startup.

## Requirements

- Python 3.x
- `requirements.txt` dependencies:
  - wmi==1.5.1
  - pywin32==305
  - colorama==0.4.6
  - pillow==9.4.0
  - infi.systray==0.1.7

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/usb-key-security-system.git
    cd USB-Key
    ```

2. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the configuration script**:

    ```bash
    python config.py
    ```

    Follow the on-screen instructions to select the USB device and set up the PIN.

## Usage

### Configuring the USB Key and PIN

Run `config.py` to configure the USB device and set up the PIN. The configuration script will:

- List all connected USB mass storage devices.
- Prompt you to select the USB device to use as the key.
- Ask you to enter a 6-digit secure PIN.
- Save a key file to the selected USB device.
- Optionally set the program to run at Windows startup.

### Running the Security System

Run `usbkey.pyw` to start the security system. The system will:

- Check if the specified USB device is connected.
- Prompt for the PIN if the USB device is connected.
- Lock the computer if the USB device is not connected or the PIN is incorrect.
- Provide system tray options to pause, continue, or quit the security check.

## Development

### Updating the USB Key Path

The `config.py` script will update the `DEVICE_PATH` variable in `usbkey.py` with the selected USB device path.

### Creating a Shortcut for Startup

The `config.py` script will also create a shortcut to `usbkey.pyw` (a copy of `usbkey.py`) in the Windows startup folder if you choose to run the program at startup.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

