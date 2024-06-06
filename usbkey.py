import os
import tkinter as tk
from tkinter import Toplevel
import time
import json
import hashlib
from infi.systray import SysTrayIcon

DEVICE_PATH = "E:"
KEY_DATA = "my_secret_key"

fullscreen_message = None
message_var = None
pause_lock = False

def check_usb():
    key_file_path = os.path.join(DEVICE_PATH, "keyfile.txt")
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as key_file:
            key_lines = key_file.readlines()
            if len(key_lines) == 2 and key_lines[0].strip() == KEY_DATA:
                return key_lines[1].strip()
    return None

def show_fullscreen_message(message):
    global fullscreen_message, message_var
    if fullscreen_message is None:
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.config(cursor='none', bg='black')
        root.title(message)

        message_var = tk.StringVar()
        message_var.set(message)
        label = tk.Label(root, textvariable=message_var, font=('Helvetica', 32), fg='white', bg='black')
        label.pack(expand=True)

        def on_closing():
            pass
        root.protocol('WM_DELETE_WINDOW', on_closing)
        root.attributes('-topmost', True)
        root.focus_force()

        root.update_idletasks()
        root.update()

        fullscreen_message = root
    else:
        message_var.set(message)

def ask_pin(parent):
    pin_window = Toplevel(parent)
    pin_window.title('secure pin')
    pin_window.geometry('300x200+600+200')
    pin_window.attributes('-topmost', True)
    pin_window.focus_force()
    
    pin_window.resizable(False, False)
    pin_window.overrideredirect(True)
    
    pin_window.configure(bg='#2e2e2e')

    label = tk.Label(pin_window, text='Enter PIN Code:', font=('Helvetica', 16), fg='white', bg='#2e2e2e')
    label.pack(pady=(20, 10))

    pin_entry = tk.Entry(pin_window, font=('Helvetica', 16), show='*', relief='flat', bg='#3e3e3e', fg='white', insertbackground='white', highlightthickness=0)
    pin_entry.pack(pady=(0, 20), ipadx=5, ipady=5)
    pin_entry.focus()

    pin_code = None

    def on_submit(event=None):
        nonlocal pin_code
        pin_code = pin_entry.get()
        pin_window.destroy()

    submit_button = tk.Button(pin_window, text='UNLOCK', command=on_submit, font=('Helvetica', 16), bg='#4CAF50', fg='white', relief='flat', activebackground='#45a049')
    submit_button.pack(ipadx=10, ipady=5)

    pin_window.bind('<Return>', on_submit)

    def on_closing():
        pass
    pin_window.protocol('WM_DELETE_WINDOW', on_closing)
    pin_window.grab_set()
    parent.wait_window(pin_window)

    return pin_code

def on_quit(systray):
    os._exit(0)

def on_pause(systray):
    global pause_lock, fullscreen_message
    pause_lock = True
    if fullscreen_message:
        fullscreen_message.destroy()
        fullscreen_message = None

def on_continue(systray):
    global pause_lock
    pause_lock = False

def main():
    global fullscreen_message, message_var, pause_lock
    stored_hashed_pin = check_usb()
    if stored_hashed_pin is None:
        show_fullscreen_message('Key Not Found')
    else:
        show_fullscreen_message('')

    def check_pin_and_unlock():
        global fullscreen_message, message_var, pause_lock
        while True:
            if pause_lock:
                time.sleep(1)
                continue
            
            if check_usb() is None:
                show_fullscreen_message('! KEY NOT FOUND !')
            else:
                if fullscreen_message:
                    pin_correct = False
                    while not pin_correct:
                        pin = ask_pin(fullscreen_message)
                        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
                        if hashed_pin == stored_hashed_pin:
                            pin_correct = True
                            fullscreen_message.destroy()
                            fullscreen_message = None
                            break
                        else:
                            message_var.set('Wrong PIN, try again.')

            while check_usb() is not None:
                time.sleep(1)
                if pause_lock:
                    break

            if check_usb() is None and not pause_lock:
                show_fullscreen_message('! KEY NOT FOUND !')

    menu_options = (("Continue Lock", None, on_continue),
                    ("Pause Lock", None, on_pause))
    systray = SysTrayIcon("icon.ico", "USB Key Checker", menu_options, on_quit=on_quit)
    systray.start()

    check_pin_and_unlock()

if __name__ == '__main__':
    main()
