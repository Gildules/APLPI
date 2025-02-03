import tkinter as tk
from tkinter import messagebox, ttk
import json
from src.io.file_io import read_tof_file
from src.processing.spectrum_processing import process_spectra, create_unique_mz_scale, align_spectra
from src.utils.helpers import create_dataframe, create_aligned_dataframe
from src.gui.settings import save_settings, load_settings
from src.gui.file_dialogs import browse_folder, browse_input_file, browse_save_file

def run_processing():
    folder_path = folder_entry.get()
    input_file = input_file_entry.get()
    mz_min = float(mz_min_entry.get())
    mz_max = float(mz_max_entry.get())
    mz_round = int(mz_round_entry.get())
    save_path = save_file_entry.get()
    algorithm = algorithm_var.get()
    enable_peak_picking = peak_picking_var.get() == 1
    peak_picking_params = {
        'signal_to_noise': float(signal_to_noise_entry.get()),
        'spacing_difference_gap': float(spacing_difference_gap_entry.get())
    }

    if not folder_path or not input_file or not save_path:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return

    if algorithm == "Интегрирование":
        integrated_spectra = process_spectra(input_file, folder_path, mz_min, mz_max, mz_round, enable_peak_picking, peak_picking_params, read_tof_file)
        unique_mz_values = create_unique_mz_scale(integrated_spectra)
        spectra_df = create_dataframe(integrated_spectra, unique_mz_values)
   
    elif algorithm == "Приведение к единой шкале":
        integrated_spectra = process_spectra(input_file, folder_path, mz_min, mz_max, mz_round, enable_peak_picking, peak_picking_params, read_tof_file)
        aligned_spectra = align_spectra(integrated_spectra, mz_min, mz_max, 1/(10**mz_round))
        spectra_df = create_aligned_dataframe(aligned_spectra)
    else:
        messagebox.showerror("Ошибка", "Неверный выбор алгоритма")
        return

    # Сохранение DataFrame в файл xlsx
    try:
        spectra_df.to_excel(save_path, index=False)
        messagebox.showinfo("Успех", f"Файл успешно сохранен: {save_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {e}")

# Создание графического интерфейса
root = tk.Tk()
root.title("Mass Spectra Integration")

tk.Label(root, text="Выберите папку:").grid(row=0, column=0, sticky=tk.W)
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Обзор...", command=lambda: browse_folder(folder_entry)).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Выберите input файл:").grid(row=1, column=0, sticky=tk.W)
input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Обзор...", command=lambda: browse_input_file(input_file_entry)).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Начальное значение m/z:").grid(row=2, column=0, sticky=tk.W)
mz_min_entry = tk.Entry(root)
mz_min_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Конечное значение m/z:").grid(row=3, column=0, sticky=tk.W)
mz_max_entry = tk.Entry(root)
mz_max_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Количество знаков при округлении m/z:").grid(row=4, column=0, sticky=tk.W)
mz_round_entry = tk.Entry(root)
mz_round_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Выберите место сохранения файла:").grid(row=5, column=0, sticky=tk.W)
save_file_entry = tk.Entry(root, width=50)
save_file_entry.grid(row=5, column=1, padx=5, pady=5)
tk.Button(root, text="Обзор...", command=lambda: browse_save_file(save_file_entry)).grid(row=5, column=2, padx=5, pady=5)

tk.Label(root, text="Выберите алгоритм:").grid(row=6, column=0, sticky=tk.W)
algorithm_var = tk.StringVar(value="Интегрирование")
ttk.Combobox(root, textvariable=algorithm_var, values=["Интегрирование", "Приведение к единой шкале"]).grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Включить выбор пиков:").grid(row=7, column=0, sticky=tk.W)
peak_picking_var = tk.IntVar()
peak_picking_check = tk.Checkbutton(root, variable=peak_picking_var)
peak_picking_check.grid(row=7, column=1, padx=5, pady=5)

tk.Label(root, text="Signal to Noise:").grid(row=8, column=0, sticky=tk.W)
signal_to_noise_entry = tk.Entry(root)
signal_to_noise_entry.grid(row=8, column=1, padx=5, pady=5)

tk.Label(root, text="Spacing Difference Gap:").grid(row=9, column=0, sticky=tk.W)
spacing_difference_gap_entry = tk.Entry(root)
spacing_difference_gap_entry.grid(row=9, column=1, padx=5, pady=5)

entries = {
    'folder_path': folder_entry,
    'input_file': input_file_entry,
    'mz_min': mz_min_entry,
    'mz_max': mz_max_entry,
    'mz_round': mz_round_entry,
    'save_path': save_file_entry,
    'algorithm': algorithm_var,
    'enable_peak_picking': peak_picking_var,
    'signal_to_noise': signal_to_noise_entry,
    'spacing_difference_gap': spacing_difference_gap_entry
}

tk.Button(root, text="Запуск обработки", command=run_processing).grid(row=10, column=0, columnspan=3, pady=10)
tk.Button(root, text="Сохранить настройки", command=lambda: save_settings(entries)).grid(row=11, column=0, columnspan=3, pady=10)
tk.Button(root, text="Загрузить настройки", command=lambda: load_settings(entries)).grid(row=12, column=0, columnspan=3, pady=10)

root.mainloop()
