import os
import subprocess
import sys

def main():
    """
    Run the Streamlit app with proper Python environment setup.
    """
    print("Starting Utility Work Planner...")
    
    # Get the absolute path to the app directory
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
    app_file = os.path.join(app_dir, "app.py")
    
    # Use python3 explicitly which seems to be in PATH
    python_executable = "python3"
    
    # Check if streamlit is installed
    try:
        subprocess.run([python_executable, "-m", "streamlit", "--version"], 
                      check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Streamlit not found. Installing required packages...")
        requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                       "requirements.txt")
        subprocess.run([python_executable, "-m", "pip", "install", "-r", requirements_path], 
                      check=True)
    
    # Add the user's python path to ensure streamlit is found
    python_user_bin = os.path.expanduser("~/Library/Python/3.9/bin")
    env = os.environ.copy()
    if 'PATH' in env:
        env['PATH'] = python_user_bin + os.pathsep + env['PATH']
    else:
        env['PATH'] = python_user_bin
    
    # Launch the Streamlit app with the updated PATH
    print(f"Launching app from {app_file}")
    try:
        streamlit_path = os.path.join(python_user_bin, "streamlit")
        if os.path.exists(streamlit_path):
            # Use the streamlit executable directly
            subprocess.run([streamlit_path, "run", app_file], env=env, check=True)
        else:
            # Fall back to module approach
            subprocess.run([python_executable, "-m", "streamlit", "run", app_file], 
                          env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching Streamlit: {e}")
        print("You can try running the app manually with:")
        print(f"cd {app_dir} && python3 -m streamlit run app.py")

if __name__ == "__main__":
    main()