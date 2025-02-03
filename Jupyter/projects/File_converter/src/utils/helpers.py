import os
import pandas as pd

def parse_filename(filename):
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    parts = name.split('_')
    
    if len(parts) != 4:
        return "error", "error", "error", "error"
    
    gas, class_, day, number = parts
    return gas, class_, day, number

def create_dataframe(spectra, unique_mz_values):
    columns = ["Filename", "Gas", "Class", "Day", "Number"] + list(unique_mz_values)
    data = []

    for filename, spectrum in spectra:
        mz_array, intensity_array = spectrum.get_peaks()
        intensity_dict = dict(zip(mz_array, intensity_array))
        gas, class_, day, number = parse_filename(filename)
        row = [filename, gas, class_, day, number] + [intensity_dict.get(mz, 0.0) for mz in unique_mz_values]
        data.append(row)

    df = pd.DataFrame(data, columns=columns)
    return df

def create_aligned_dataframe(aligned_spectra):
    mz_values = aligned_spectra[0][1]
    columns = ["Filename", "Gas", "Class", "Day", "Number"] + list(mz_values)
    data = []

    for filename, _, intensity_aligned in aligned_spectra:
        gas, class_, day, number = parse_filename(filename)
        row = [filename, gas, class_, day, number] + list(intensity_aligned)
        data.append(row)

    df = pd.DataFrame(data, columns=columns)
    return df
