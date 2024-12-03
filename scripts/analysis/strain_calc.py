import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Constants
wavelength = 632.8e-9  # Wavelength of the laser in meters
I0 = 1  # Maximum intensity (assuming normalized intensity)
arm_length = 1.43  # Length of the interferometer arm in meters
error_intensity = 0.025  # 0.5% error on intensity measurements
error_length = 0.025  # 0.5% error on length measurements

def normalize_intensity(intensity):
    """
    Normalize the signal intensity to a range between 0 and 1.

    Parameters:
    - intensity: Signal intensity array

    Returns:
    - normalized_intensity: Normalized intensity array
    """
    min_intensity = np.min(intensity)
    max_intensity = np.max(intensity)
    normalized_intensity = (intensity - min_intensity) / (max_intensity - min_intensity)
    return normalized_intensity

def calculate_displacement(intensity):
    """
    Calculate the displacement of the moving mirror as a function of the signal intensity.

    Parameters:
    - intensity: Signal intensity array

    Returns:
    - displacement: Displacement array in meters
    """
    displacement = (wavelength / (4 * np.pi)) * np.arccos((intensity - I0) / I0)
    return displacement

def calculate_strain(displacement, arm_length):
    """
    Calculate the strain as a function of the displacement.

    Parameters:
    - displacement: Displacement array in meters
    - arm_length: Length of the interferometer arm in meters

    Returns:
    - strain: Strain array
    """
    strain = displacement / arm_length
    return strain

def error_propagation(intensity, displacement, arm_length):
    """
    Perform error propagation to calculate the error in strain.

    Parameters:
    - intensity: Signal intensity array
    - displacement: Displacement array in meters
    - arm_length: Length of the interferometer arm in meters

    Returns:
    - error_strain: Error in strain array
    """
    error_displacement = (wavelength / (4 * np.pi)) * (1 / np.sqrt(1 - ((intensity - I0) / I0)**2)) * error_intensity
    error_strain = np.sqrt((error_displacement / arm_length)**2 + (displacement * error_length / arm_length**2)**2)
    return error_strain

def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    - file_path: Path to the CSV file

    Returns:
    - time: Time array
    - intensity: Intensity array
    """
    data = pd.read_csv(file_path)
    time = data['Time'].values
    intensity = data['Signal'].values
    return time, intensity

def plot_strain(time, strain, error_strain, output_path=None):
    """
    Plot the strain with error lines.

    Parameters:
    - time: Time array
    - strain: Strain array
    - error_strain: Error in strain array
    - output_path: Path to save the plot image (if None, display the plot)
    """
    # Remove points with infinite values in the error
    finite_mask = np.isfinite(error_strain)
    time_finite = time[finite_mask]
    strain_finite = strain[finite_mask]
    error_strain_finite = error_strain[finite_mask]

    plt.figure(figsize=(10, 6))
    plt.plot(time_finite, strain_finite, label='Strain')
    
    # Calculate the positive and negative error curves
    strain_plus = strain_finite + error_strain_finite
    strain_minus = strain_finite - error_strain_finite

    plt.plot(time_finite, strain_plus, label='Positive Error', linestyle='--', color='grey', linewidth = 0.5)
    plt.plot(time_finite, strain_minus, label='Negative Error', linestyle='--', color='grey', linewidth = 0.5)

    plt.title('Strain of the Interferometer Arm with Error Lines')
    plt.xlabel('Time')
    plt.ylabel('Strain')
    plt.grid(True)
    plt.legend()
    
    if output_path:
        plt.savefig(output_path)
        plt.close()
        print(f"Saved plot to {output_path}")
    else:
        plt.show()

def process_datasets(input_dir, output_dir):
    """
    Process all datasets in the input directory and save the plots to the output directory.

    Parameters:
    - input_dir: Path to the input directory containing CSV files
    - output_dir: Path to the output directory to save plot images
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # List of dataset filenames
    dataset_filenames = [f"Dataset_{i}.CSV" for i in range(1, 5)]

    for filename in dataset_filenames:
        file_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_strain.png")

        # Load data
        time, intensity = load_data(file_path)

        # Normalize the intensity
        normalized_intensity = normalize_intensity(intensity)

        # Calculate the displacement
        displacement = calculate_displacement(normalized_intensity)

        # Calculate the strain
        strain = calculate_strain(displacement, arm_length)

        # Perform error propagation
        error_strain = error_propagation(normalized_intensity, displacement, arm_length)

        # Plot the strain with error lines
        plot_strain(time, strain, error_strain, output_path)

        # Print the first few strain values and their errors
        print(f"Strain values for {filename}: {strain[:5]}")
        print(f"Error in strain for {filename}: {error_strain[:5]}")

# Example usage
input_dir = '../../data/FinalData'
output_dir = '../../data/FinalData/Strain_Plots'
process_datasets(input_dir, output_dir)