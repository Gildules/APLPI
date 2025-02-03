import numpy as np
import os
from pyopenms import MSSpectrum

def process_spectra(input_file, folder_path, mz_min, mz_max, mz_round, enable_peak_picking, peak_picking_params, read_tof_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    integrated_spectra = []

    for line in lines:
        parts = line.strip().split()
        
        if len(parts) < 3 or not parts[1].isdigit():
            print(f"Неверный формат строки: {line}")
            continue

        filename = parts[0]
        num_ranges = int(parts[1])
        ranges = []

        try:
            for i in range(num_ranges):
                start = int(parts[i * 2 + 2])
                end = int(parts[i * 2 + 3])
                ranges.append((start, end))
        except (IndexError, ValueError) as e:
            print(f"Ошибка при разборе диапазонов в строке: {line}")
            print(f"Ошибка: {e}")
            continue

        filepath = os.path.join(folder_path, filename)
        experiment = read_tof_file(filepath, enable_peak_picking, peak_picking_params)

        for start, end in ranges:
            spectra_to_integrate = experiment.getSpectra()[start:end+1]
            
            integrated_mz = {}
            for spectrum in spectra_to_integrate:
                for peak in spectrum:
                    mz = round(peak.getMZ(), mz_round)
                    if mz_min <= mz <= mz_max:
                        intensity = peak.getIntensity()
                        if mz in integrated_mz:
                            integrated_mz[mz] += intensity
                        else:
                            integrated_mz[mz] = intensity
            
            if integrated_mz:
                mz_list = sorted(integrated_mz.keys())
                intensity_list = [integrated_mz[mz] for mz in mz_list]
                integrated_spectrum = MSSpectrum()
                integrated_spectrum.set_peaks([np.array(mz_list), np.array(intensity_list)])
                integrated_spectrum.setRT(float(start))
                integrated_spectrum.setMSLevel(spectra_to_integrate[0].getMSLevel())
                integrated_spectra.append((filename, integrated_spectrum))

    return integrated_spectra

def create_unique_mz_scale(spectra):
    mz_values = set()
    for _, spectrum in spectra:
        mz_array, _ = spectrum.get_peaks()
        mz_values.update(mz_array)
    unique_mz_values = sorted(mz_values)
    return unique_mz_values

def align_spectra(spectra, mz_min, mz_max, mz_step):
    aligned_spectra = []
    mz_aligned = np.arange(mz_min, mz_max, mz_step)

    for filename, spectrum in spectra:
        mz_array, intensity_array = spectrum.get_peaks()
        intensity_aligned = np.interp(mz_aligned, mz_array, intensity_array, left=0, right=0)
        
        aligned_spectrum = (filename, mz_aligned, intensity_aligned)
        aligned_spectra.append(aligned_spectrum)

    return aligned_spectra
