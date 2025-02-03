import os
import numpy as np
import struct
from pyopenms import MSExperiment, MSSpectrum, SpectrumAlignment, PeakPickerHiRes, Param

def read_tof_file(filepath, enable_peak_picking, peak_picking_params):
    with open(filepath, 'rb') as fid:
        fid.seek(278)
        numMS = struct.unpack('I', fid.read(4))[0]
        numPn = struct.unpack('I', fid.read(4))[0]

        fid.seek(286)
        AA = struct.unpack('d', fid.read(8))[0]
        BB = struct.unpack('d', fid.read(8))[0]

        zz_read = AA * ((np.arange(numPn)) + BB) ** 2
        fid.seek(512)
        MS_1 = np.zeros((numMS, numPn), dtype=int)

        fi_t1 = 0x4000
        fi_t2 = 0x8000
        fi_t3 = 0xc000
        fi_3f = 0x3fff

        experiment = MSExperiment()
        aligner = SpectrumAlignment()
        params = aligner.getParameters()
        params.setValue("tolerance", 0.1)
        params.setValue("is_relative_tolerance", "true")
        aligner.setParameters(params)

        peak_picker = PeakPickerHiRes()
        if enable_peak_picking:
            picker_params = Param()
            picker_params.setValue("signal_to_noise", peak_picking_params['signal_to_noise'])
            picker_params.setValue("spacing_difference_gap", peak_picking_params['spacing_difference_gap'])
            peak_picker.setParameters(picker_params)

        for ii in range(numMS):
            arr = np.zeros(numPn, dtype=int)
            i1, i0, nB = 1, 1, 1

            npPack = struct.unpack('I', fid.read(4))[0]
            Buf_pack = np.frombuffer(fid.read(npPack * 2), dtype=np.uint16)
            nbArrP = struct.unpack('I', fid.read(4))[0]
            Buf_MS = np.frombuffer(fid.read(nbArrP), dtype=np.uint8)

            for p in range(npPack):
                fi_type = Buf_pack[p]
                type = fi_type & fi_t3
                c = fi_type & fi_3f

                i1 = i0 + c

                if type == fi_t1:
                    arr[i0-1:i1-1] = Buf_MS[nB-1:nB+i1-i0-1]
                    nB += i1 - i0
                elif type == fi_t2:
                    idx_range = np.arange(nB-1, nB+2*(i1-i0-1), 2)
                    if len(idx_range) > len(arr[i0-1:i1-1]):
                        idx_range = idx_range[:len(arr[i0-1:i1-1])]
                    arr[i0-1:i1-1] = Buf_MS[idx_range] + 256*Buf_MS[idx_range + 1]
                    nB += 2 * (i1 - i0)
                elif type == fi_t3:
                    idx_range = np.arange(nB-1, nB+4*(i1-i0-1), 4)
                    if len(idx_range) > len(arr[i0-1:i1-1]):
                        idx_range = idx_range[:len(arr[i0-1:i1-1])]
                    arr[i0-1:i1-1] = Buf_MS[idx_range] + 256*Buf_MS[idx_range + 1] + \
                                     65536*Buf_MS[idx_range + 2] + 16777216*Buf_MS[idx_range + 3]
                    nB += 4 * (i1 - i0)

                i0 = i1

            MS_1[ii, :] = arr

            spectrum = MSSpectrum()
            spectrum.setMSLevel(1)
            spectrum.set_peaks([zz_read, arr])

            if enable_peak_picking:
                picked_spectrum = MSSpectrum()
                peak_picker.pick(spectrum, picked_spectrum)
                spectrum = picked_spectrum

            if ii > 0:  # Выравнивание начиная со второго спектра
                prev_spectrum = experiment.getSpectrum(ii - 1)
                alignment = []
                aligner.getSpectrumAlignment(alignment, prev_spectrum, spectrum)
                # Внести необходимые изменения в спектр на основе alignment (если нужно)

            experiment.addSpectrum(spectrum)

    return experiment
