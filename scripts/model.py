import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path, signal_column):
    """
    Load data from a CSV file.

    Parameters:
    - file_path: Path to the CSV file
    - signal_column: Name of the column containing the signal data

    Returns:
    - time: Time array
    - signal: Signal array
    """
    data = pd.read_csv(file_path)
    time = data['Path Difference (micrometers)'].values
    signal = data[signal_column].values
    return time, signal

def plot_data(time, combined_signal, output_path=None):
    """
    Plot the combined signal.

    Parameters:
    - time: Time array
    - combined_signal: Combined signal array
    - output_path: Path to save the plot image (if None, display the plot)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, combined_signal, label='Combined Signal')
    plt.title('Combined Interference Pattern and Noise')
    plt.xlabel('Path Difference (micrometers)')
    plt.ylabel('Signal')
    plt.legend()
    plt.grid(True)
    
    if output_path:
        plt.savefig(output_path)
        plt.close()
        print(f"Saved plot to {output_path}")
    else:
        plt.show()

# Load data from CSV files
time_interference, interference_pattern = load_data('../data/interference_pattern.csv', 'Intensity')
time_noise, noise = load_data('../data/noise.csv', 'Noise')

# Ensure the time arrays are the same
if not np.array_equal(time_interference, time_noise):
    raise ValueError("Time arrays from the two files do not match.")

# Add the interference pattern and noise together
combined_signal = interference_pattern + noise

# Plot the combined signal
plot_data(time_interference, combined_signal, output_path='../data/combined_signal_plot.png')

# Print the first few values of the combined signal
print("First few values of the combined signal:")
print(combined_signal[:5])