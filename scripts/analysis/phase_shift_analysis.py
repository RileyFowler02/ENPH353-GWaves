'''
Overview: Analyzing change in voltage (light intensity) due to phase shifts between the two light paths.

Goal for the output: 
- Measure small displacements or vibrations in the arm
- Detection of environmental changes like temperature or pressure shifts
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def phase_shift_analysis(path_diff, combined_signal, wavelength=500e-9):
    """
    Perform phase shift analysis on the combined signal to measure small displacements or vibrations.

    Parameters:
    - path_diff: Path difference array
    - combined_signal: Combined signal array
    - wavelength: Wavelength of the light source in meters (default is 500 nm)

    Returns:
    - phase_shifts: Phase shifts array
    """
    # Calculate the phase shifts
    phase_shifts = np.arccos((combined_signal - 1) / 1) * wavelength / (2 * np.pi)
    return phase_shifts

def plot_phase_shifts(path_diff, phase_shifts):
    """
    Plot the phase shifts.

    Parameters:
    - path_diff: Path difference array
    - phase_shifts: Phase shifts array
    """
    plt.figure(figsize=(10, 6))
    plt.plot(path_diff, phase_shifts, label='Phase Shifts')
    plt.title('Phase Shifts Analysis')
    plt.xlabel('Path Difference (micrometers)')
    plt.ylabel('Phase Shifts (meters)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Example usage
interference_csv = './data/interference_pattern.csv'
noise_csv = './data/noise.csv'

# Load data
path_diff, intensity, noise = load_data(interference_csv, noise_csv)

# Combine signal with noise
combined_signal = combine_signal_with_noise(intensity, noise)

# Perform phase shift analysis
phase_shifts = phase_shift_analysis(path_diff, combined_signal)

# Plot phase shifts
plot_phase_shifts(path_diff, phase_shifts)