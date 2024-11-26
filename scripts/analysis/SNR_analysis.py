'''
Goal: Analyzing the Signal-to-Noise Ratio (SNR) to determine the quality of the signal

Output:
- Determine the quality of the signal as a ratio of the signal power to the noise power
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import glob
import os
import logging

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

def high_pass_filter(signal, cutoff, fs, order=5):
    """
    Apply a high-pass filter to isolate the noise.

    Parameters:
    - signal: Input signal array
    - cutoff: Cutoff frequency for the high-pass filter
    - fs: Sampling frequency
    - order: Order of the filter (default is 5)

    Returns:
    - filtered_signal: Filtered signal array (noise)
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

def calculate_snr(signal, noise):
    """
    Calculate the Signal-to-Noise Ratio (SNR).

    Parameters:
    - signal: Signal array
    - noise: Noise array

    Returns:
    - snr: Signal-to-Noise Ratio in dB
    """
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def calculate_average_power_ratio(signal, noise):
    """
    Calculate the average power ratio between the noise and the signal.

    Parameters:
    - signal: Signal array
    - noise: Noise array

    Returns:
    - power_ratio: Average power ratio (noise power / signal power)
    """
    signal_power = np.mean(signal ** 2)
    noise_power = np.mean(noise ** 2)
    power_ratio = noise_power / signal_power
    return power_ratio

def plot_signal_and_noise(time, signal, noise, output_path, title='Signal and Noise'):
    """
    Plot the signal and noise.

    Parameters:
    - time: Time array
    - signal: Signal array
    - noise: Noise array
    - output_path: Path to save the plot image
    - title: Title of the plot
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, signal, label='Signal')
    plt.plot(time, noise, label='Noise', linestyle='--')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot to {output_path}")

def process_files(input_dir, output_dir, cutoff_frequency, sampling_frequency, output_file):
    """
    Process all CSV files in the input directory and save the analysis results to an output file.

    Parameters:
    - input_dir: Path to the input directory containing CSV files
    - output_dir: Path to the output directory to save plot images
    - cutoff_frequency: Cutoff frequency for the high-pass filter in Hz
    - sampling_frequency: Sampling frequency in Hz
    - output_file: Path to the output CSV file to save analysis results
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_dir, '*.csv')) + glob.glob(os.path.join(input_dir, '*.CSV'))

    if not csv_files:
        logging.info(f"No CSV files found in {input_dir}")
        return

    results = []

    for file_path in csv_files:
        try:
            # Load data
            time, signal = load_data(file_path)

            # Estimate noise using a high-pass filter
            estimated_noise = high_pass_filter(signal, cutoff_frequency, sampling_frequency)

            # Calculate SNR
            snr = calculate_snr(signal, estimated_noise)

            # Calculate average power ratio
            power_ratio = calculate_average_power_ratio(signal, estimated_noise)

            # Append results
            results.append({
                'File': os.path.basename(file_path),
                'SNR (dB)': snr,
                'Average Power Ratio (Noise/Signal)': power_ratio
            })

            # Plot signal and noise
            output_plot_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(file_path))[0]}_plot.png")
            plot_signal_and_noise(time, signal, estimated_noise, output_plot_path, title=f'Signal and Noise from {os.path.basename(file_path)}')

            logging.info(f"Processed {file_path}")

        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")

    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    logging.info(f"Saved analysis results to {output_file}")

# Example usage
input_dir = '../../data/FinalData'
output_dir = '../../data/FinalData/SNR_Plots'
cutoff_frequency = 50  # Cutoff frequency for the high-pass filter in Hz
sampling_frequency = 1000  # Sampling frequency in Hz
output_file = '../../data/FinalData/SNR_results.csv'
process_files(input_dir, output_dir, cutoff_frequency, sampling_frequency, output_file)