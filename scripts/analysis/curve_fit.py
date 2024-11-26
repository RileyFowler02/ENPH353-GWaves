import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import glob

def sine(x, amp, freq, phase):
    """
    Sine function with amplitude, frequency, and phase parameters.

    Parameters:
    - x: Input array
    - amp: Amplitude of the sine wave
    - freq: Frequency of the sine wave
    - phase: Phase shift of the sine wave

    Returns:
    - Sine wave output
    """
    offset = -0.5  # Fixed offset
    return amp * np.sin(2 * np.pi * freq * x + phase) + offset

def fit_sine(time, signal):
    """
    Fit a sine wave to the given data with a fixed offset.

    Parameters:
    - time: Time array
    - signal: Signal array

    Returns:
    - popt: Optimal values for the parameters
    - pcov: Covariance of the parameters
    """
    # Initial guess for the parameters
    guess_amplitude = 6  # np.std(signal) * 2**0.5
    guess_frequency = 450
    guess_phase = np.pi / 4
    p0 = [guess_amplitude, guess_frequency, guess_phase]

    # Fit the sine wave
    popt, pcov = curve_fit(sine, time, signal, p0=p0)
    return popt, pcov

def plot_fit(time, signal, popt, output_path):
    """
    Plot the original signal and the fitted sine wave.

    Parameters:
    - time: Time array
    - signal: Signal array
    - popt: Optimal values for the parameters
    - output_path: Path to save the plot image
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, signal, label='Original Signal')
    plt.plot(time, sine(time, *popt), label='Fitted Sine Wave', linestyle='--')
    plt.title('Sine Wave Fitting')
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot to {output_path}")

def process_files(input_dir, output_dir):
    """
    Process all CSV files in the input directory and save the plots to the output directory.

    Parameters:
    - input_dir: Path to the input directory containing CSV files
    - output_dir: Path to the output directory to save plot images
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_dir, 'Dataset_*.CSV'))

    for file_path in csv_files:
        # Load data
        data = pd.read_csv(file_path)
        time = data['Time'].values
        signal = data['Signal'].values

        # Fit a sine wave to the data
        popt, pcov = fit_sine(time, signal)

        # Generate output plot path
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_fit.png")

        # Plot the original data and the fitted sine wave
        plot_fit(time, signal, popt, output_path)

        # Print the optimal parameters
        print(f"Optimal parameters for {file_name}: Amplitude={popt[0]}, Frequency={popt[1]}, Phase={popt[2]}, Offset=-0.5")

# Example usage
input_dir = '../../data/FinalData'
output_dir = '../../data/FinalData/CF_Plots'
process_files(input_dir, output_dir)