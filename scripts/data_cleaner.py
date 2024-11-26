import pandas as pd
import glob
import os

def clean_and_load_csv(file_path, output_path):
    """
    Clean the CSV file by removing the header data and load the time and signal data.

    Parameters:
    - file_path: Path to the CSV file
    - output_path: Path to save the cleaned CSV file

    Returns:
    - time: Time array
    - signal: Signal array
    """
    try:
        # Read the CSV file
        data = pd.read_csv(file_path, header=None, skiprows=3, usecols=[3, 4], names=['Time', 'Signal'])

        # Drop rows with NaN values
        data.dropna(inplace=True)

        # Save the cleaned data to a new CSV file
        data.to_csv(output_path, index=False)

        # Extract time and signal arrays
        time = data['Time'].values
        signal = data['Signal'].values

        return time, signal
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def process_directory(input_dir, output_dir):
    """
    Process all CSV files in the input directory and save cleaned files to the output directory.

    Parameters:
    - input_dir: Path to the input directory containing dirty CSV files
    - output_dir: Path to the output directory to save cleaned CSV files
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all CSV files in the input directory (case-insensitive)
    csv_files = glob.glob(os.path.join(input_dir, '*.csv')) + glob.glob(os.path.join(input_dir, '*.CSV'))

    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    for file_path in csv_files:
        # Generate the output file path
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_dir, file_name)

        # Clean and load the CSV file
        time, signal = clean_and_load_csv(file_path, output_path)
        if time is not None and signal is not None:
            print(f"Processed {file_path} -> {output_path}")
        else:
            print(f"Failed to process {file_path}")

# Example usage
input_dir = '../data/DirtyData'
output_dir = '../data/CleanData'
process_directory(input_dir, output_dir)