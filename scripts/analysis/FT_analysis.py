'''
Goal: Creating a Fourier Transform (FT) analysis to analyze the frequency components of the signal with drift

Output:
- Finding at which frequencies noise is minimized/maximized
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    - file_path: Path to the CSV file

    Returns:
    - time: Time array
    - signal: Signal array
    """
    data = pd.read_csv(file_path)
    time = data['Time'].values
    signal = data['Signal'].values
    return time, signal

def fourier_transform_analysis(signal, sampling_rate):
    """
    Perform Fourier Transform analysis on the input signal.

    Parameters:
    - signal: Input time-domain signal
    - sampling_rate: Sampling rate of the signal

    Returns:
    - freqs: Frequencies corresponding to the FT
    - magnitude: Magnitude of the FT
    """
    n = len(signal)
    window = np.hanning(n)  # Apply a Hanning window to the signal
    signal_windowed = signal * window
    freqs = np.fft.fftfreq(n, d=1/sampling_rate)
    ft = np.fft.fft(signal_windowed)
    magnitude = np.abs(ft) / n
    return freqs, magnitude

def plot_frequency_spectrum(freqs, magnitude, output_path=None):
    """
    Plot the frequency spectrum of the signal and optionally save the plot as an image.

    Parameters:
    - freqs: Frequencies corresponding to the FT
    - magnitude: Magnitude of the FT
    - output_path: Path to save the plot image (if None, display the plot)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, magnitude)
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    
    if output_path:
        plt.savefig(output_path)
        plt.close()
        print(f"Saved plot to {output_path}")
    else:
        plt.show()

def process_datasets(input_dir, output_dir, sampling_rate, save_plots):
    """
    Process all datasets in the input directory and save or display the frequency spectrum plots.

    Parameters:
    - input_dir: Path to the input directory containing CSV files
    - output_dir: Path to the output directory to save plot images
    - sampling_rate: Sampling rate of the signal
    - save_plots: Boolean indicating whether to save the plots to files or display them
    """
    # Ensure the output directory exists if saving plots
    if save_plots:
        os.makedirs(output_dir, exist_ok=True)

    # List of dataset filenames
    dataset_filenames = [f"Dataset_{i}.CSV" for i in range(1, 5)]

    for filename in dataset_filenames:
        file_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_spectrum.png") if save_plots else None

        try:
            # Load data
            time, signal = load_data(file_path)

            # Perform Fourier Transform analysis
            freqs, magnitude = fourier_transform_analysis(signal, sampling_rate)

            # Plot the frequency spectrum
            plot_frequency_spectrum(freqs, magnitude, output_path)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# Example usage
input_dir = '../../data/FinalData'
output_dir = '../../data/FinalData/Plots'
sampling_rate = 1000  # Assuming a sampling rate of 1000 Hz for the example

# Prompt the user whether to save the plots or display them
save_plots_input = input("Do you want to save the plots to files? (yes/no): ").strip().lower()
save_plots = save_plots_input == 'yes'

process_datasets(input_dir, output_dir, sampling_rate, save_plots)