import os
import sys
import cv2
import argparse
import platform
import signal
import tkinter as tk
from tkinter import messagebox

# macOS M1 specific fixes: limit threads before torch import (if used)
if any(arg.startswith('--execution-provider') for arg in sys.argv):
    os.environ['OMP_NUM_THREADS'] = '1'

# Dummy globals simulation (replace with your actual globals)
class Globals:
    execution_providers = []
    headless = False
    lang = 'en'
    source_path = None
    target_path = None
    output_path = None

modules = type('modules', (), {'globals': Globals()})

def list_cameras(max_devices=5):
    """Try to open camera devices to detect available indices."""
    available = []
    for i in range(max_devices):
        cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

def camera_test(device_index=0):
    """Test opening the camera and show live feed."""
    print(f"Opening camera device {device_index}...")
    cap = cv2.VideoCapture(device_index, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print("Failed to open camera.")
        return False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            break
        cv2.imshow('FaceTime Camera Test (press ESC to quit)', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return True

def destroy():
    print("Cleanup and exit")
    sys.exit(0)

def init_ui(start_callback, destroy_callback, lang):
    """Basic Tkinter window to simulate your UI init."""
    root = tk.Tk()
    root.title("Deep-Live-Cam Demo")
    root.geometry("400x200")

    label = tk.Label(root, text="Deep-Live-Cam GUI Running", font=("Arial", 16))
    label.pack(pady=20)

    btn_start = tk.Button(root, text="Start Camera Test", command=start_callback)
    btn_start.pack(pady=10)

    btn_quit = tk.Button(root, text="Quit", command=destroy_callback)
    btn_quit.pack(pady=10)

    return root

def start():
    print("Starting camera test...")
    cams = list_cameras()
    print(f"Available cameras: {cams}")
    if not cams:
        print("No cameras found.")
        messagebox.showerror("Error", "No cameras detected. Please check permissions.")
        return

    # Try first available camera
    if not camera_test(cams[0]):
        messagebox.showerror("Error", "Could not open the camera.")
        return

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execution-provider', dest='execution_provider', default=['coreml'], nargs='+',
                        choices=['cpu', 'coreml', 'cuda', 'rocm'])
    args = parser.parse_args()
    modules.globals.execution_providers = args.execution_provider
    modules.globals.headless = False  # force GUI for demo
    print(f"Using execution providers: {modules.globals.execution_providers}")

def main():
    parse_args()

    # macOS camera permission reminder
    if platform.system() == 'Darwin':
        print("Reminder: Make sure Terminal has Camera access under System Settings -> Privacy & Security -> Camera")

    # Run GUI or headless
    if modules.globals.headless:
        print("Running headless (no GUI)")
        start()
    else:
        print("Running with GUI")
        window = init_ui(start, destroy, modules.globals.lang)
        window.mainloop()

if __name__ == '__main__':
    main()
