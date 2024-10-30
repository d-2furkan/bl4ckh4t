import asyncio
import aiohttp
import sys
import platform
import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Function to print the header in green
def print_header():
    print(Fore.GREEN + "="*35)
    print(Fore.GREEN + "   Subdomain Finder & Scanner Tool   ")
    print(Fore.GREEN + "="*35)
    print(Fore.GREEN + "Coded by  : Darkboy")
    print(Fore.GREEN + "Design by : KAIRO")
    print(Fore.GREEN + "Telegram  : @Darkboy336")
    print(Fore.GREEN + "Version   : 1.1")
    print(Fore.GREEN + "="*35, "\n")

# Function to print user information in green
def print_user_info():
    os_info = platform.system()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    timezone = datetime.datetime.now().astimezone().tzinfo
    print(Fore.GREEN + "USER INFORMATION")
    print(Fore.GREEN + "OS        :", os_info)
    print(Fore.GREEN + "Date      :", current_date)
    print(Fore.GREEN + "Time      :", current_time)
    print(Fore.GREEN + "Timezone  :", timezone)
    print(Fore.GREEN + "Country   : India")
    print(Fore.GREEN + "="*35, "\n")

# Function to display options in green
def print_options():
    print(Fore.GREEN + "Choose an option (1/2/3):")
    print(Fore.GREEN + "[1] - Find Subdomains")
    print(Fore.GREEN + "[2] - Scan Subdomains")
    print(Fore.GREEN + "[3] - Exit Program")
    print(Fore.GREEN + "="*35, "\n")

# Asynchronous function to check HTTP status for a given domain using HEAD method
async def check_http_head(session, target_domain):
    url = f"http://{target_domain}"
    try:
        async with session.head(url, timeout=5, allow_redirects=False) as response:
            server_header = response.headers.get('Server', 'Unknown')
            
            # Check for redirection
            if 'Location' in response.headers:
                redirect_url = response.headers['Location']
                output = f"HEAD\t{response.status}\t{server_header}\t{target_domain} -> {redirect_url}"
            else:
                output = f"HEAD\t{response.status}\t{server_header}\t{target_domain}"

            # Color code based on response status
            if 200 <= response.status < 400:
                return Fore.GREEN + output  # Success statuses in green
            else:
                return output  # Non-successful statuses in default color
    
    except Exception:
        return Fore.RED + f"HEAD\tError\tUnknown\t{target_domain}"  # Errors in red

# Function to read targets from a text file
def read_targets(file_path):
    try:
        with open(file_path, 'r') as file:
            targets = file.read().splitlines()
        return targets
    except FileNotFoundError:
        print(Fore.RED + "File not found. Please check the file path.")
        sys.exit(1)

# Asynchronous function to scan domains concurrently
async def scan_domains_concurrently(domains, max_connections=100):
    connector = aiohttp.TCPConnector(limit=max_connections)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_http_head(session, domain) for domain in domains]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(result)

# Main execution
if __name__ == "__main__":
    print_header()
    print_user_info()
    print_options()
    
    option = input("Enter an option (1/2/3): ")
    
    if option == "2":
        file_path = input("Enter file to scan subdomains: ")
        targets = read_targets(file_path)
        
        print(Fore.GREEN + "\nScanning subdomains from:", file_path)
        print(Fore.GREEN + "="*50)
        
        # Run the asynchronous scanning function
        asyncio.run(scan_domains_concurrently(targets))
        
        print(Fore.GREEN + "="*50)
    elif option == "1":
        print(Fore.RED + "Subdomain finding feature is not implemented in this script.")
    elif option == "3":
        print(Fore.GREEN + "Exiting the program.")
    else:
        print(Fore.RED + "Invalid option. Please enter 1, 2, or 3.")
