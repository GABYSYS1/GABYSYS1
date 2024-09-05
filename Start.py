import os
import sys
import time
import subprocess
import requests

def print_colored(text, color_code):
    os.system(f"echo \x1b[{color_code}m{text}\x1b[0m")

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
        print_colored(f"Package '{package}' installed successfully.", "32")
    except subprocess.CalledProcessError as e:
        print_colored(f"Failed to install '{package}': {e}", "31")
        sys.exit(1)

def check_and_install_packages():
    """Check and install required packages."""
    required_packages = ['requests', 'beautifulsoup4', 'selenium', 'webdriver-manager', 'psutil', 'colorama', 'docx']
    for package in required_packages:
        try:
            __import__(package)
            print_colored(f"Package '{package}' is already installed.", "32")
        except ImportError:
            print_colored(f"Package '{package}' is not installed. Installing...", "33")
            install_package(package)

def download_file(url, filename):
    """Download a file from a URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        with open(filename, 'wb') as file:
            file.write(response.content)
        print_colored(f"{filename} downloaded successfully.", "32")  # Green text
    except requests.exceptions.RequestException as e:
        print_colored(f"Failed to download {filename}: {e}", "31")  # Red text
        sys.exit(1)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Step 1: Clear the screen and display initial messages
    clear_screen()
    ip = requests.get('https://api.ipify.org').text
    print_colored(f"Running 'Start.py'", "36")  # Cyan text
    print_colored(f"Hello {os.getlogin()}! Or should I call you: {ip}", "37")  # White text
    print_colored("Installing Packages...", "32")
    time.sleep(1)
    
    # Step 2: Check and install required packages
    check_and_install_packages()
    
    print_colored("Getting dependencies...", "32")
    time.sleep(1)
    
    # Step 3: Download vertex.py from GitHub
    print_colored("Downloading vertex...", "32")
    vertex_url = "https://raw.githubusercontent.com/GABYSYS1/GABYSYS1/main/vertex.py"  # Adjust the path if necessary
    download_file(vertex_url, "vertex.py")
    
    # Step 4: Clear screen again for clarity
    clear_screen()
    
    # Step 5: Execute vertex.py with error handling
    print_colored("Launching vertex...", "35")
    time.sleep(1)
    try:
        subprocess.run([sys.executable, "vertex.py"], check=True)
    except subprocess.CalledProcessError as e:
        print_colored(f"Error executing vertex.py: {e}", "31")  # Red text
        print_colored(f"Standard output:\n{e.stdout}", "31")
        print_colored(f"Standard error:\n{e.stderr}", "31")
        print_colored("Ensure that vertex.py is properly configured and all dependencies are installed.", "31")
    except Exception as e:
        print_colored(f"Unexpected error occurred: {e}", "31")

if __name__ == "__main__":
    main()
