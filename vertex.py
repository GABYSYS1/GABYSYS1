import os
import sys
import socket
import time
import subprocess
import psutil

# Function to print colored text in CMD
def print_colored(text, color_code):
    os.system(f"echo \x1b[{color_code}m{text}\x1b[0m")

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_message():
    print_colored("Running 'Vertex.py'", "36")  # Cyan text
    user_name = os.getlogin()
    user_ip = socket.gethostbyname(socket.gethostname())
    print_colored(f"Hello {user_name}! Your IP: {user_ip}", "37")  # White text

def list_all_files():
    print_colored("\nListing all files on your PC...", "32")
    directories = [
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Downloads'),
        os.path.expanduser('~\\Music'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Videos'),
        'C:\\Users\\Public\\Desktop',
        'C:\\Program Files',
        'C:\\Program Files (x86)',
        'C:\\Windows\\System32'
    ]
    count = 0
    for directory in directories:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    count += 1
                    print(f"{count}. {os.path.join(root, file)}")
    if count == 0:
        print_colored("No files found.", "31")

def list_processes():
    print_colored("\nListing all running processes with PID...", "32")
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"PID: {proc.info['pid']} - Name: {proc.info['name']}")

def end_process():
    pid = input("Enter the PID of the process to end (or type 'back' to return): ")
    if pid.lower() == 'back':
        return
    try:
        psutil.Process(int(pid)).terminate()
        print_colored(f"Process {pid} terminated successfully.", "32")
    except Exception as e:
        print_colored(f"Error terminating process: {e}", "31")

def run_command():
    command = input("Enter the Windows command to run (or type 'back' to return): ")
    if command.lower() == 'back':
        return
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print_colored(f"Error: {e.output.decode()}", "31")

def show_websites():
    websites = {
        1: "https://www.google.com",
        2: "https://www.youtube.com",
        3: "https://www.facebook.com",
        4: "https://www.amazon.com",
        5: "https://www.wikipedia.org"
    }
    print_colored("\nAvailable websites to open:", "32")
    for num, site in websites.items():
        print(f"{num}. {site}")
    choice = input("Enter the number of the website to open (or type 'back' to return): ")
    if choice.lower() == 'back':
        return
    try:
        choice = int(choice)
        if choice in websites:
            os.startfile(websites[choice])
        else:
            print_colored("Invalid choice. Please try again.", "31")
    except ValueError:
        print_colored("Invalid input. Please enter a number.", "31")

def system_info():
    try:
        output = subprocess.check_output('systeminfo', shell=True)
        print(output.decode())
    except Exception as e:
        print_colored(f"Error retrieving system info: {e}", "31")

def change_password():
    choice = input("1. Change your own password\n2. Change another user's password (Admin required)\nEnter your choice (1-2): ")
    if choice == '1':
        new_password = input("Enter your new password: ")
        if new_password:
            command = f"net user {os.getlogin()} {new_password}"
            try:
                subprocess.check_output(command, shell=True)
                print_colored("Password changed successfully.", "32")
            except subprocess.CalledProcessError:
                print_colored("Failed to change password. Are you running as an admin?", "31")
    elif choice == '2':
        user_list = subprocess.check_output('net user', shell=True).decode()
        print(user_list)
        user = input("Enter the username to change password for: ")
        new_password = input(f"Enter the new password for {user}: ")
        if new_password:
            command = f"net user {user} {new_password}"
            try:
                subprocess.check_output(command, shell=True)
                print_colored("Password changed successfully.", "32")
            except subprocess.CalledProcessError:
                print_colored("Failed to change password. Ensure you have administrative privileges.", "31")

def backup_files():
    print_colored("Backing up files... (Not Implemented)", "33")

def main_menu():
    clear_screen()
    while True:
        print_colored("\n========================", "32")
        print_colored("      Command Menu      ", "32")
        print_colored("========================", "32")
        print("1. List Processes")
        print("2. End Process")
        print("3. Run Windows Command")
        print("4. Show Websites")
        print("5. Open File")
        print("6. System Information")
        print("7. Backup Files")
        print("8. Change Password")
        print("9. Exit")
        print_colored("========================", "32")
        
        choice = input("Enter your choice (1-9): ")
        
        if choice == '1':
            list_processes()
        elif choice == '2':
            end_process()
        elif choice == '3':
            run_command()
        elif choice == '4':
            show_websites()
        elif choice == '5':
            list_all_files()
        elif choice == '6':
            system_info()
        elif choice == '7':
            backup_files()
        elif choice == '8':
            change_password()
        elif choice == '9':
            print_colored("Exiting VERTEX. Goodbye!", "32")
            break
        else:
            print_colored("Invalid choice. Please try again.", "31")

if __name__ == "__main__":
    welcome_message()
    main_menu()
