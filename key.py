
import tkinter as tk
from datetime import datetime
from pathlib import Path


LOG_FILE = Path("keylogger_lab.log")


def write_to_file(timestamp, key):
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(f"{timestamp}  {key}\n")


def key_pressed(event):
    key = event.keysym

    # Make special keys readable
    if key == "space":
        key = "[SPACE]"
    elif key == "Return":
        key = "[ENTER]"
    elif key == "BackSpace":
        key = "[BACKSPACE]"
    elif key == "Tab":
        key = "[TAB]"
    elif key == "Escape":
        key = "[ESC]"
    elif len(key) > 1:
        key = f"[{key.upper()}]"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Display in the application
    log.insert(tk.END, f"{timestamp}  {key}\n")
    log.see(tk.END)

    # Save to file
    write_to_file(timestamp, key)


def clear_screen():
    log.delete("1.0", tk.END)


def show_log_location():
    location_label.config(
        text=f"Log file: {LOG_FILE.absolute()}"
    )


root = tk.Tk()
root.title("Python Keylogger Lab")
root.geometry("700x500")

title = tk.Label(
    root,
    text="PYTHON KEYLOGGER LAB",
    font=("Arial", 20, "bold")
)
title.pack(pady=15)

instruction = tk.Label(
    root,
    text="Click inside this window and type something.",
    font=("Arial", 11)
)
instruction.pack()

log = tk.Text(
    root,
    font=("Consolas", 12),
    width=70,
    height=18
)
log.pack(padx=20, pady=15)

button_frame = tk.Frame(root)
button_frame.pack()

clear_button = tk.Button(
    button_frame,
    text="Clear Screen",
    command=clear_screen
)
clear_button.pack(side=tk.LEFT, padx=5)

location_button = tk.Button(
    button_frame,
    text="Show Log Location",
    command=show_log_location
)
location_button.pack(side=tk.LEFT, padx=5)

location_label = tk.Label(
    root,
    text="Logging enabled → keylogger_lab.log",
    font=("Arial", 9)
)
location_label.pack(pady=10)

# IMPORTANT:
# This only listens for keyboard events inside this application.
root.bind("<KeyPress>", key_pressed)

root.mainloop()

