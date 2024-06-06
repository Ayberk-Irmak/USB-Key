import wmi
import os
import hashlib
import getpass
import shutil
from win32com.client import Dispatch
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_usb_mass_storage_devices():
    c = wmi.WMI()
    usb_list = []
    for drive in c.Win32_DiskDrive():
        if 'USB' in drive.PNPDeviceID:
            for partition in drive.associators("Win32_DiskDriveToDiskPartition"):
                for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                    usb_list.append({
                        'DeviceID': logical_disk.DeviceID,
                        'Caption': drive.Caption,
                        'PNPDeviceID': drive.PNPDeviceID
                    })
    return usb_list

def select_usb_device(usb_list):
    print(f"{Fore.BLUE}[INFO] - USB mass storage devices:")
    for index, device in enumerate(usb_list):
        print(f"{index + 1}: {device['Caption']} ({device['DeviceID']})")
    
    choice = int(input("Enter the number of the USB device you want to use: ")) - 1
    return usb_list[choice]

def get_pin():
    while True:
        pin = getpass.getpass("Enter the 6-digit secure PIN code(The entered numbers will not appear in the console):")
        if len(pin) == 6 and pin.isdigit():
            return pin
        else:
            print(f"{Fore.YELLOW}[INFO] - The PIN code must be 6 digits long and consist of numbers only.")

def save_key_file(device, pin):
    key_data = "my_secret_key"
    hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
    key_file_path = os.path.join(device['DeviceID'], "keyfile.txt")
    with open(key_file_path, 'w') as key_file:
        key_file.write(f"{key_data}\n{hashed_pin}")
    print(f"{Fore.GREEN}[SUCCESS] - The key file was written to {key_file_path}.")

def update_usbkey_py(device):
    with open('usbkey.py', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open('usbkey.py', 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip().startswith('DEVICE_PATH ='):
                file.write(f'DEVICE_PATH = "{device["DeviceID"]}"\n')
            else:
                file.write(line)

def create_shortcut():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_path = os.path.abspath('usbkey.pyw')
    shutil.copy('usbkey.py', script_path)
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(os.path.join(startup_folder, "usbkey.lnk"))
    shortcut.TargetPath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.IconLocation = script_path
    shortcut.save()
    print(f"{Fore.GREEN}[SUCCESS] - The program is configured to run at startup: {script_path}")

def main():
    clear_console()
    
    usb_list = list_usb_mass_storage_devices()
    if not usb_list:
        print(f"{Fore.RED}[ERROR] - No USB mass storage device found.")
        return
    
    selected_device = select_usb_device(usb_list)
    update_usbkey_py(selected_device)
    pin = get_pin()
    save_key_file(selected_device, pin)
    print(f"{Fore.GREEN}[SUCCESS] - Selected USB device: {selected_device['Caption']}")

    choice = input("Do you want the program to start automatically with Windows? (Y/n): ").strip().lower()
    if choice == 'y':
        create_shortcut()
    else:
        script_path = os.path.abspath('usbkey.pyw')
        shutil.copy('usbkey.py', script_path)
        

if __name__ == '__main__':
    main()
