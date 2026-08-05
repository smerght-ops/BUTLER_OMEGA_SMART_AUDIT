import subprocess
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LAUNCHER = ROOT / "_RFC_WORK" / "launchers" / "START_SAFE_LAUNCH.py"

process = None

def start_system():
    global process
    log("STARTING SYSTEM...")

    process = subprocess.Popen(["python", str(LAUNCHER)])

    log("SYSTEM RUNNING")

def stop_system():
    global process
    if process:
        process.terminate()
        log("SYSTEM STOPPED")

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# UI
app = tk.Tk()
app.title("BUTLER OMEGA CONTROL PANEL")
app.geometry("600x400")

title = tk.Label(app, text="BUTLER OMEGA", font=("Arial", 18))
title.pack(pady=10)

start_btn = tk.Button(app, text="START SYSTEM", bg="green", fg="white", command=start_system)
start_btn.pack(pady=5)

stop_btn = tk.Button(app, text="STOP SYSTEM", bg="red", fg="white", command=stop_system)
stop_btn.pack(pady=5)

log_box = scrolledtext.ScrolledText(app, width=70, height=15)
log_box.pack(pady=10)

log("UI READY")

app.mainloop()
