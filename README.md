## Instructions to set-up the virtual environment

For the first time setting up the repo:

1. **Navigate to project directory** (if you aren't already in it):
   - For Mac/Linux: Open terminal and run:
     ```sh
     cd /path/to/project/location
     ```
   - For Windows: Open Command Prompt or PowerShell and run:
     ```sh
     cd \path\to\project\location
     ```
You can check if you are in the correct directory using `pwd` (present working directory)

2. **Set up the [.venv] directory**:
   - Run the following command to create a virtual environment named [.venv]:
     ```sh
     python3 -m venv .venv  # For Mac/Linux
     # or
     python -m venv .venv  # For Windows
     ```

3. **Activate the virtual environment**:
   - On Mac/Linux:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .\.venv\Scripts\activate
     ```

4. **Install basic libraries**:
   - Once the virtual environment is activated, install the required libraries using `pip`:
     ```sh
     pip install -r requirements.txt
     ```

Currently these libraries are just the ones I usually use (i.e., scipy, matplot, etc) but I'm sure there are others that could be useful. 

5. **Deactivate the virtual environment** (when done working):
   - Run the following command to deactivate the virtual environment:
     ```sh
     deactivate
     ```