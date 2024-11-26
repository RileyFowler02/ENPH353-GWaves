import matplotlib.pyplot as plt
import pandas as pd
import glob
import os

def plot_csv(file_path, output_dir):
    """
    Plot the data from a CSV file and save the plot as an image.

    Parameters:
    - file_path: Path to the CSV file
    - output_dir: Directory to save the plot images
    """
    try:
        # Read the CSV file
        data = pd.read_csv(file_path)

        # Extract time and signal columns
        time = data['Time']
        signal = data['Signal']

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(time, signal, label='Signal')
        plt.title(f'Signal from {os.path.basename(file_path)}')
        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.legend()
        plt.grid(True)

        # Save the plot as an image
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        output_path = os.path.join(output_dir, f"{file_name}.png")
        plt.savefig(output_path)
        plt.close()
        print(f"Saved plot to {output_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(input_dir, output_dir):
    """
    Process all CSV files in the input directory and save plots to the output directory.

    Parameters:
    - input_dir: Path to the input directory containing CSV files
    - output_dir: Path to the output directory to save plot images
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all CSV files in the input directory (case-insensitive)
    csv_files = glob.glob(os.path.join(input_dir, '*.csv')) + glob.glob(os.path.join(input_dir, '*.CSV'))

    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    for file_path in csv_files:
        plot_csv(file_path, output_dir)

# Example usage
input_dir = '../data/CleanData'
output_dir = '../data/Plots'
process_directory(input_dir, output_dir)