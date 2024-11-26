'''
Goal: Analyzing the fluctuations in intensity to find coherence properties in the light source

Output:
- Determine the stability of the laser
- Quantify noise in the system
- Quantify phase stability over time
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

def amplitude_analysis(combined_signal):
    """
    Perform amplitude analysis on the combined signal to find coherence properties.

    Parameters:
    - combined_signal: Combined signal array

    Returns:
    - mean_intensity: Mean intensity of the signal
    - std_intensity: Standard deviation of the intensity (quantifies noise)
    - phase_stability: Phase stability over time (quantified by standard deviation)
    """
    mean_intensity = np.mean(combined_signal)
    std_intensity = np.std(combined_signal)
    phase_stability = std_intensity / mean_intensity  # Relative phase stability

    return mean_intensity, std_intensity, phase_stability

def plot_intensity_fluctuations(path_diff, combined_signal):
    """
    Plot the intensity fluctuations of the combined signal.

    Parameters:
    - path_diff: Path difference array
    - combined_signal: Combined signal array
    """
    plt.figure(figsize=(10, 6))
    plt.plot(path_diff, combined_signal, label='Combined Signal')
    plt.title('Intensity Fluctuations')
    plt.xlabel('Path Difference (micrometers)')
    plt.ylabel('Intensity')
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

# Perform amplitude analysis
mean_intensity, std_intensity, phase_stability = amplitude_analysis(combined_signal)

# Print results
print(f"Mean Intensity: {mean_intensity}")
print(f"Standard Deviation of Intensity: {std_intensity}")
print(f"Phase Stability (Relative): {phase_stability}")

# Plot intensity fluctuations
plot_intensity_fluctuations(path_diff, combined_signal)