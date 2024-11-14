import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def generate_interference_pattern(length1, length2, wavelength=500e-9, output_csv='interference_pattern.csv'):
    """
    Generate and plot the interference pattern for a Michelson interferometer and export the data to a CSV file.

    Parameters:
    - length1: Length of the first path in meters
    - length2: Length of the second path in meters
    - wavelength: Wavelength of the light source in meters (default is 500 nm)
    - output_csv: Filename for the output CSV file (default is 'interference_pattern.csv')
    """
    # Calculate the path difference
    path_difference = length1 - length2

    # Define a range of path differences around the calculated path difference
    path_diff_range = np.linspace(path_difference - 2e-6, path_difference + 2e-6, 1000)

    # Calculate the interference pattern
    I0 = 1  # Maximum intensity
    intensity = I0 * (1 + np.cos(2 * np.pi * path_diff_range / wavelength))

    # Plot the interference pattern
    plt.figure(figsize=(10, 6))
    plt.plot(path_diff_range * 1e6, intensity)  # Convert path difference to micrometers for plotting
    plt.title('Interference Pattern of a Michelson Interferometer')
    plt.xlabel('Path Difference (micrometers)')
    plt.ylabel('Intensity')
    plt.grid(True)
    plt.show()

    # Export the data to a CSV file
    data = {
        'Path Difference (micrometers)': path_diff_range * 1e6,
        'Intensity': intensity
    }
    df = pd.DataFrame(data)
    df.to_csv('./data/interference_pattern.csv', index=False)

# Example usage
length1 = 1.0  # Length of the first path in meters
length2 = 1.000001  # Length of the second path in meters
generate_interference_pattern(length1, length2)