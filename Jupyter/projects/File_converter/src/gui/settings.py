import json
from tkinter import filedialog, messagebox
import tkinter as tk
def save_settings(entries):
    settings = {}
    for key, entry in entries.items():
        if isinstance(entry, tk.Entry):
            settings[key] = entry.get()
        elif isinstance(entry, tk.StringVar):
            settings[key] = entry.get()
        elif isinstance(entry, tk.IntVar):
            settings[key] = entry.get()
    file_selected = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_selected:
        with open(file_selected, 'w') as f:
            json.dump(settings, f)
        messagebox.showinfo("Успех", f"Настройки успешно сохранены: {file_selected}")

def load_settings(entries):
    file_selected = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_selected:
        with open(file_selected, 'r') as f:
            settings = json.load(f)
        for key, entry in entries.items():
            value = settings.get(key, '')
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif isinstance(entry, tk.StringVar):
                entry.set(value)
            elif isinstance(entry, tk.IntVar):
                entry.set(int(value))
        messagebox.showinfo("Успех", f"Настройки успешно загружены: {file_selected}")
