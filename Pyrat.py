import socket
import threading
import time

# ANSI escape codes for colors
RESET = "\033[0m"
GREEN = "\033[92m"  # Bright green

# Welcoming message
print("Welcome to the Password Fuzzer!")
print("This script will help you test passwords against a specified endpoint.")
print("Instructions:")
print("1. Provide the target IP address and port where the service is running.")
print("2. Specify the path to your password wordlist (e.g., '/usr/share/wordlists/rockyou.txt').")
print("3. Enter the endpoint (e.g., 'admin') where you want to test the passwords.")
print("4. The script will attempt each password and notify you when a correct password is found.")
print("5. Status updates will be printed every 10 seconds until a successful password is found.\n")

# Configuration
target_ip = input("Enter the target IP: ")
target_port = int(input("Enter the target port: "))
password_wordlist = input("Enter the path to the password wordlist: ")
endpoint = input("Enter the endpoint to fuzz (e.g., 'admin'): ")

# Track the success flag
success_flag = False

def connect_and_send_password(password):
    global success_flag
    if success_flag:  # If a successful password has been found, stop trying
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((target_ip, target_port))
        client_socket.sendall(f'{endpoint}\n'.encode())

        response = client_socket.recv(1024).decode()

        if "Password:" in response:  # If the server asks for a password
            print(f"Trying password: {password}")
            client_socket.sendall(password.encode() + b"\n")

            response = client_socket.recv(1024).decode()

            # Check if the password was accepted
            if "Success" in response or "Welcome" in response or "Logged in" in response:
                print(f"{GREEN}Correct password found: {password}{RESET}")  # Use bright green for success message
                success_flag = True  # Mark the success flag
            else:
                print(f"Password '{password}' was incorrect or no response.")
        else:
            print("Did not receive a password prompt.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def fuzz_passwords():
    global success_flag
    with open(password_wordlist, "r", encoding="latin-1") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()  # Remove any newline characters

        if success_flag:  # If a successful password was found, stop
            break

        connect_and_send_password(password)

def status_message():
    while not success_flag:  # Only run if no successful password is found yet
        print("Still fuzzing passwords...")
        time.sleep(10)  # Print status every 10 seconds

if __name__ == "__main__":
    # Start the status message in a separate thread
    status_thread = threading.Thread(target=status_message)
    status_thread.daemon = True  # Daemonize the thread to exit when the main program finishes
    status_thread.start()

    # Start fuzzing passwords
    fuzz_passwords()

    # After fuzzing finishes
    if success_flag:
        print("Password fuzzing completed successfully.")
    else:
        print("No valid password was found.")
