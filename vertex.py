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

init(autoreset=True)  # Automatically reset colors after each print

# Discord bot token and channel ID
DISCORD_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
DISCORD_CHANNEL_ID = 'YOUR_CHANNEL_ID_HERE'

def print_colored(text, color):
    """Print text in the specified color."""
    print(f"{color}{text}{Style.RESET_ALL}")

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    else:
        print_colored("No Word, PowerPoint, or Excel files found.", Fore.RED)
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
            else:
                print_colored("Invalid choice. Please try again.", Fore.RED)
        except ValueError:
            print_colored("Invalid input. Please enter a number.", Fore.RED)
    else:
        print_colored("No Word, PowerPoint, or Excel files found to open.", Fore.RED)
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
                else:
                    print_colored(f"Invalid choice: {file_index + 1}. Skipping.", Fore.RED)

            # Send a message to Discord after backing up files
            send_discord_message(f"User '{os.getlogin()}' backed up files to '{backup_folder}'.")

        except ValueError:
            print_colored("Invalid input. Please enter valid numbers.", Fore.RED)
    else:
        print_colored("No Word, PowerPoint, or Excel files found to backup.", Fore.RED)
    input("\nPress Enter to return to the menu...")

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

def list_processes():
    clear_screen()
    print_colored("\n========================", Fore.GREEN)
    print_colored("   List Processes Menu  ", Fore.YELLOW)
    print_colored("========================", Fore.GREEN)
    print("1. Sort by Name (A-Z)")
    print("2. Sort by Memory Usage (Descending)")
    print("3. Back to Menu")
    print_colored("========================", Fore.GREEN)

    sort_choice = input("Enter your choice (1-3): ")

    if sort_choice == '1':
        sort_by_name()
    elif sort_choice == '2':
        sort_by_memory_usage()
    elif sort_choice == '3':
        return
    else:
        print_colored("Invalid choice. Please try again.", Fore.RED)
        input("\nPress Enter to continue...")
        list_processes()

def sort_by_name():
    clear_screen()
    print_colored("\n========================", Fore.GREEN)
    print_colored("Processes Sorted by Name (A-Z)", Fore.YELLOW)
    print_colored("========================", Fore.GREEN)
    print(f"{'Name':<25} {'PID':<10} {'Memory Usage':<15}")
    print(f"{'-'*25} {'-'*10} {'-'*15}")

    processes = [(proc.info['name'], proc.info['pid'], proc.info['memory_info'].rss) for proc in psutil.process_iter(['name', 'pid', 'memory_info'])]
    sorted_processes = sorted(processes, key=lambda x: x[0].lower())

    for process in sorted_processes:
        name, pid, memory = process
        print(f"{name:<25} {pid:<10} {memory / 1024 / 1024:.2f} MB")

    input("\nPress Enter to return to the menu...")

def sort_by_memory_usage():
    clear_screen()
    print_colored("\n========================", Fore.GREEN)
    print_colored("Processes Sorted by Memory Usage (Descending)", Fore.YELLOW)
    print_colored("========================", Fore.GREEN)
    print(f"{'Name':<25} {'PID':<10} {'Memory Usage':<15}")
    print(f"{'-'*25} {'-'*10} {'-'*15}")

    processes = [(proc.info['name'], proc.info['pid'], proc.info['memory_info'].rss) for proc in psutil.process_iter(['name', 'pid', 'memory_info'])]
    sorted_processes = sorted(processes, key=lambda x: x[2], reverse=True)

    for process in sorted_processes:
        name, pid, memory = process
        print(f"{name:<25} {pid:<10} {memory / 1024 / 1024:.2f} MB")

    input("\nPress Enter to return to the menu...")

def end_process():
    clear_screen()
    pid = input("Enter the PID of the process to end (or type 'back' to return): ")
    if pid.lower() == 'back':
        return
    try:
        psutil.Process(int(pid)).terminate()
        print_colored(f"Process {pid} terminated successfully.", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error terminating process: {e}", Fore.RED)
    input("\nPress Enter to return to the menu...")

def run_command():
    clear_screen()
    command = input("Enter the Windows command to run (or type 'back' to return): ")
    if command.lower() == 'back':
        return
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print_colored(f"Error: {e.output.decode()}", Fore.RED)
    input("\nPress Enter to return to the menu...")

def show_websites():
    clear_screen()
    websites = {
        1: "https://www.google.com",
        2: "https://www.youtube.com",
        3: "https://www.facebook.com",
        4: "https://www.amazon.com",
        5: "https://www.wikipedia.org",
        6: "https://www.twitter.com",
        7: "https://www.instagram.com",
        8: "https://www.reddit.com",
        9: "https://www.netflix.com",
        10: "https://www.yahoo.com",
        11: "https://www.ebay.com",
        12: "https://www.twitch.tv",
        13: "https://www.microsoft.com",
        14: "https://www.zoom.us",
        15: "https://www.apple.com",
        16: "https://www.tiktok.com",
        17: "https://www.bing.com",
        18: "https://www.pinterest.com",
        19: "https://www.walmart.com",
        20: "https://www.craigslist.org",
        21: "https://www.espn.com",
        22: "https://www.cnn.com",
        23: "https://www.bbc.com",
        24: "https://www.nytimes.com",
        25: "https://www.github.com",
        26: "https://www.stackoverflow.com",
        27: "https://www.linkedin.com",
        28: "https://www.whatsapp.com",
        29: "https://www.messenger.com",
        30: "https://www.discord.com",
        31: "https://www.spotify.com",
        32: "https://www.steam.com",
        33: "https://www.adobe.com",
        34: "https://www.dropbox.com",
        35: "https://www.flickr.com",
        36: "https://www.vimeo.com",
        37: "https://www.tumblr.com",
        38: "https://www.paypal.com"
    }
    print_colored("\nAvailable websites to open:", Fore.GREEN)
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
            print_colored("Invalid choice. Please try again.", Fore.RED)
    except ValueError:
        print_colored("Invalid input. Please enter a number.", Fore.RED)
    input("\nPress Enter to return to the menu...")

def system_info():
    clear_screen()
    try:
        output = subprocess.check_output('systeminfo', shell=True)
        print(output.decode())
    except Exception as e:
        print_colored(f"Error retrieving system info: {e}", Fore.RED)
    input("\nPress Enter to return to the menu...")

def change_password():
    clear_screen()
    new_password = input("Enter your new password: ")
    if new_password:
        command = f"net user {os.getlogin()} {new_password}"
        try:
            subprocess.check_output(command, shell=True)
            print_colored("Password changed successfully.", Fore.GREEN)
        except subprocess.CalledProcessError:
            print_colored("Failed to change password. Ensure you're running the script as a regular user and not an administrator.", Fore.RED)
    input("\nPress Enter to return to the menu...")

def id_resolver():
    clear_screen()
    """Resolve Discord user ID to a username using Selenium to interact with discord.id."""
    discord_user_id = input("Enter the Discord user ID to resolve: ")
    
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no browser UI)
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to discord.id
        driver.get("https://discord.id/")

        # Wait for the input box to be available
        wait = WebDriverWait(driver, 20)
        input_box = wait.until(EC.presence_of_element_located((By.ID, 'userid')))

        # Enter the Discord user ID
        input_box.clear()
        input_box.send_keys(discord_user_id)
        input_box.send_keys(Keys.RETURN)

        # Wait for the result to appear
        wait.until(EC.presence_of_element_located((By.ID, 'userTag')))

        # Extract the username
        result = driver.find_element(By.ID, 'userTag')
        username = result.text.strip()
        if username:
            print_colored(f"Discord Username: {username}", Fore.GREEN)
        else:
            print_colored("No results found. Please check the Discord ID.", Fore.RED)
    except Exception as e:
        print_colored(f"Error resolving Discord ID: {e}", Fore.RED)
    finally:
        driver.quit()

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
    except Exception as e:
        print_colored(f"Error clearing cache: {e}", Fore.RED)
    input("\nPress Enter to return to the menu...")

def show_active_window_title():
    clear_screen()
    try:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        h_wnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(h_wnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(h_wnd, buffer, length + 1)
        print_colored(f"Active Window Title: {buffer.value}", Fore.GREEN)
    except Exception as e:
        print_colored(f"Error retrieving active window title: {e}", Fore.RED)
    input("\nPress Enter to return to the menu...")

def main_menu():
    while True:
        clear_screen()
        display_header()
        display_menu()
        display_socials()
        
        choice = input("Enter your choice (1-14): ")
        
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
            break
        else:
            print_colored("Invalid choice. Please try again.", Fore.RED)

if __name__ == "__main__":
    main_menu()
