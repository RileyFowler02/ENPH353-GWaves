import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Constants
wavelength = 632.8e-9  # Wavelength of the laser in meters
I0 = 1  # Maximum intensity (assuming normalized intensity)
arm_length = 1.0  # Length of the interferometer arm in meters

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

def plot_strain(time, strain, output_path=None):
    """
    Plot the strain.

    Parameters:
    - time: Time array
    - strain: Strain array
    - output_path: Path to save the plot image (if None, display the plot)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, strain)
    plt.title('Strain of the Interferometer Arm')
    plt.xlabel('Time')
    plt.ylabel('Strain')
    plt.grid(True)
    
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

        # Plot the strain
        plot_strain(time, strain, output_path)

        # Print the first few strain values
        print(f"Strain values for {filename}: {strain[:5]}")

# Example usage
input_dir = '../../data/FinalData'
output_dir = '../../data/FinalData/Strain_Plots'
process_datasets(input_dir, output_dir)