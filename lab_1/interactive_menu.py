import tkinter as tk
from tkinter import messagebox
import json
import os
from typing import Any

def task_1() -> None:
    """Display the encrypted text from the first file."""
    try:
        with open(settings['encrypted_text_1'], 'r', encoding='utf-8') as file:
            encrypted_text = file.read()
        messagebox.showinfo("Encrypted Text", encrypted_text)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")

def task_2() -> None:
    """Display the text from the second file."""
    try:
        with open(settings['encrypted_text_2'], 'r', encoding='utf-8') as file:
            text = file.read()
        messagebox.showinfo("Text from File", text)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")


with open(os.path.join('settings.json'), 'r', encoding='utf-8') as settings_file:
    settings: dict[str, Any] = json.load(settings_file)

root = tk.Tk()
root.title("Task Execution")

image_path = "chifer.png"
background_image = tk.PhotoImage(file=image_path)

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

buttons_frame = tk.Frame(root)
buttons_frame.pack(expand=True, padx=20, pady=20)

button_task_1 = tk.Button(buttons_frame, text="Task 1: Decrypt Text", command=task_1, font=("Arial", 14))
button_task_2 = tk.Button(buttons_frame, text="Task 2: Display Text", command=task_2, font=("Arial", 14))

button_task_1.pack(fill=tk.X, pady=10)
button_task_2.pack(fill=tk.X, pady=10)

root.mainloop()
