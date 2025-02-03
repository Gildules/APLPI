from tkinter import filedialog 
import tkinter as tk
def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry.delete(0, tk.END)
        entry.insert(0, folder_selected)

def browse_input_file(entry):
    file_selected = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_selected:
        entry.delete(0, tk.END)
        entry.insert(0, file_selected)

def browse_save_file(entry):
    file_selected = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_selected:
        entry.delete(0, tk.END)
        entry.insert(0, file_selected)
