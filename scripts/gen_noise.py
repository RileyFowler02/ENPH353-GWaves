'''
Goal: Generate a noise floor
Output: CSV file containing the noise floor data
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_noise_floor(length1, length2, noise_level=0.1):
    """
    Generate, plot, and export the noise floor data for a Michelson interferometer.

    Parameters:
    - length1: Length of the first path in meters
    - length2: Length of the second path in meters
    - wavelength: Wavelength of the light source in meters (default is 500 nm)
    - noise_level: Amplitude of the noise (default is 0.1)
    - output_csv: Filename for the output CSV file (default is 'noise_floor.csv')
    """
    # Calculate the path difference
    path_difference = length1 - length2

    # Define a range of path differences around the calculated path difference
    path_diff_range = np.linspace(path_difference - 2e-6, path_difference + 2e-6, 1000)

    # Generate the noise floor
    noise = noise_level * np.random.randn(len(path_diff_range))

    # Plot the noise floor
    plt.figure(figsize=(10, 6))
    plt.plot(path_diff_range * 1e6, noise, label='Noise Floor')
    plt.title('Noise Floor of a Michelson Interferometer')
    plt.xlabel('Path Difference (micrometers)')
    plt.ylabel('Noise')
    plt.grid(True)
    plt.legend()
    plt.show()

    # Export the noise data to a CSV file
    data = {
        'Path Difference (micrometers)': path_diff_range * 1e6,
        'Noise': noise
    }
    df = pd.DataFrame(data)
    df.to_csv('./data/noise.csv', index=False)

# Example usage
length1 = 1.0  # Length of the first path in meters
length2 = 1.000001  # Length of the second path in meters
generate_noise_floor(length1, length2)