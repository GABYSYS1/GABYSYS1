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

# Discord bot token and channel ID
DISCORD_BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
DISCORD_CHANNEL_ID = 'YOUR_CHANNEL_ID_HERE'

# Function to print colored text in CMD
def print_colored(text, color_code):
    os.system(f"echo \x1b[{color_code}m{text}\x1b[0m")

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the header with ASCII art and instructions."""
    print_colored(r"""
  _    __     ______  _______  __  __ 
 | |  / /    |  ____||__   __||  \/  |
 | | / /     | |__      | |   | \  / |
 | |/ /      |  __|     | |   | |\/| |
 |   <       | |____    | |   | |  | |
 |_|\_\      |______|   |_|   |_|  |_|        
    """, "36")  # Cyan text for VERTEX in ASCII art

def display_menu():
    """Display the main menu."""
    print_colored("\n========================", "32")  # Green text for section separator
    print_colored("      Command Menu      ", "33")  # Yellow text for menu title
    print_colored("========================", "32")
    print_colored("1. List Processes", "34")  # Blue text for menu items
    print_colored("2. End Process", "34")
    print_colored("3. Run Windows Command", "34")
    print_colored("4. Show Websites", "34")
    print_colored("5. Open File", "34")
    print_colored("6. System Information", "34")
    print_colored("7. Backup Files", "34")
    print_colored("8. Change Password", "34")
    print_colored("9. ID Resolver", "34")
    print_colored("10. Exit", "34")
    print_colored("========================", "32")

def display_socials():
    """Display social media information below the menu."""
    print_colored("\nMy socials:", "35")  # Magenta text for "My socials:"
    print_colored("Made by Fraise Le BG", "35")
    print_colored("Youtube: https://www.youtube.com/@PWEBIDUOS", "35")
    print_colored("Discord: Discord.com/", "35")

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
    print_colored("\nListing all Word, PowerPoint, and Excel files on your PC...", "32")
    files = list_files_by_type(('.docx', '.pptx', '.xlsx'))
    if files:
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")
    else:
        print_colored("No Word, PowerPoint, or Excel files found.", "31")
    input("\nPress Enter to return to the menu...")

def open_file():
    clear_screen()
    print_colored("\nSelect a file to open (only Word, PowerPoint, and Excel files):", "32")
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
                print_colored("Invalid choice. Please try again.", "31")
        except ValueError:
            print_colored("Invalid input. Please enter a number.", "31")
    else:
        print_colored("No Word, PowerPoint, or Excel files found to open.", "31")
    input("\nPress Enter to return to the menu...")

def backup_files():
    clear_screen()
    print_colored("\nSelect files to backup (only Word, PowerPoint, and Excel files):", "32")
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
                    print_colored(f"File {files[file_index]} backed up successfully.", "32")
                else:
                    print_colored(f"Invalid choice: {file_index + 1}. Skipping.", "31")

            # Send a message to Discord after backing up files
            send_discord_message(f"User '{os.getlogin()}' backed up files to '{backup_folder}'.")

        except ValueError:
            print_colored("Invalid input. Please enter valid numbers.", "31")
    else:
        print_colored("No Word, PowerPoint, or Excel files found to backup.", "31")
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
        print_colored("Notification sent to Discord.", "32")
    else:
        print_colored(f"Failed to send message to Discord: {response.status_code} - {response.text}", "31")

def list_processes():
    clear_screen()
    print_colored("\n========================", "32")
    print_colored("   List Processes Menu  ", "32")
    print_colored("========================", "32")
    print("1. Sort by Name (A-Z)")
    print("2. Sort by Memory Usage (Descending)")
    print("3. Back to Menu")
    print_colored("========================", "32")

    sort_choice = input("Enter your choice (1-3): ")

    if sort_choice == '1':
        sort_by_name()
    elif sort_choice == '2':
        sort_by_memory_usage()
    elif sort_choice == '3':
        return
    else:
        print_colored("Invalid choice. Please try again.", "31")
        input("\nPress Enter to continue...")
        list_processes()

def sort_by_name():
    clear_screen()
    print_colored("\n========================", "32")
    print_colored("Processes Sorted by Name (A-Z)", "32")
    print_colored("========================", "32")
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
    print_colored("\n========================", "32")
    print_colored("Processes Sorted by Memory Usage (Descending)", "32")
    print_colored("========================", "32")
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
        print_colored(f"Process {pid} terminated successfully.", "32")
    except Exception as e:
        print_colored(f"Error terminating process: {e}", "31")
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
        print_colored(f"Error: {e.output.decode()}", "31")
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
    input("\nPress Enter to return to the menu...")

def system_info():
    clear_screen()
    try:
        output = subprocess.check_output('systeminfo', shell=True)
        print(output.decode())
    except Exception as e:
        print_colored(f"Error retrieving system info: {e}", "31")
    input("\nPress Enter to return to the menu...")

def change_password():
    clear_screen()
    new_password = input("Enter your new password: ")
    if new_password:
        command = f"net user {os.getlogin()} {new_password}"
        try:
            subprocess.check_output(command, shell=True)
            print_colored("Password changed successfully.", "32")
        except subprocess.CalledProcessError:
            print_colored("Failed to change password. Ensure you're running the script as a regular user and not an administrator.", "31")
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
            print_colored(f"Discord Username: {username}", "32")
        else:
            print_colored("No results found. Please check the Discord ID.", "31")
    except Exception as e:
        print_colored(f"Error resolving Discord ID: {e}", "31")
    finally:
        driver.quit()

def main_menu():
    while True:
        clear_screen()
        display_header()
        display_menu()
        display_socials()
        
        choice = input("Enter your choice (1-10): ")
        
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
            print_colored("Exiting VERTEX. Goodbye!", "32")
            break
        else:
            print_colored("Invalid choice. Please try again.", "31")

if __name__ == "__main__":
    main_menu()
