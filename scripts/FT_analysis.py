'''
Goal: Creating a Fourier Transform (FT) analysis to analyze the frequency components of the signal with drift

Output:
- Finding at which frequencies noise is minimized/maximized
'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_data(interference_csv, noise_csv):
    """
    Load interference pattern and noise data from CSV files.

    Parameters:
    - interference_csv: Path to the interference pattern CSV file
    - noise_csv: Path to the noise CSV file

    Returns:
    - path_diff: Path difference array
    - intensity: Intensity array
    - noise: Noise array
    """
    interference_data = pd.read_csv(interference_csv)
    noise_data = pd.read_csv(noise_csv)

    path_diff = interference_data['Path Difference (micrometers)'].values
    intensity = interference_data['Intensity'].values
    noise = noise_data['Noise'].values

    return path_diff, intensity, noise

def combine_signal_with_noise(intensity, noise):
    """
    Combine the interference pattern intensity with noise.

    Parameters:
    - intensity: Intensity array of the interference pattern
    - noise: Noise array

    Returns:
    - combined_signal: Combined signal array
    """
    combined_signal = intensity + noise
    return combined_signal

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
    freqs = np.fft.fftfreq(n, d=1/sampling_rate)
    ft = np.fft.fft(signal)
    magnitude = np.abs(ft) / n
    return freqs, magnitude

def plot_frequency_spectrum(freqs, magnitude):
    """
    Plot the frequency spectrum of the signal.

    Parameters:
    - freqs: Frequencies corresponding to the FT
    - magnitude: Magnitude of the FT
    """
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, magnitude)
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.show()

# Example usage
interference_csv = './data/interference_pattern.csv'
noise_csv = './data/noise.csv'

# Load data
path_diff, intensity, noise = load_data(interference_csv, noise_csv)

# Combine signal with noise
combined_signal = combine_signal_with_noise(intensity, noise)

# Perform Fourier Transform analysis
sampling_rate = 1000  # Assuming a sampling rate of 1000 Hz for the example
freqs, magnitude = fourier_transform_analysis(combined_signal, sampling_rate)

# Plot the frequency spectrum
plot_frequency_spectrum(freqs, magnitude)