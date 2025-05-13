# ToolSSHed
Toolkit for SSH pentesting(Check version, bruteforce and password spraying)
### This tool was developed for use strictly in educational labs and/or authorized ambients, unauthorized or illegal use is NOT promoted or encouraged.

## Requirements
Libraries used:
- paramiko
- argparsed
- socket
- concurrent.futures

## Usage
  -h, --help                         Show this help message and exit
  
  -i, --ip                           Target machine IP
  
  -u, --username                     Username for bruteforcing
  
  -p, --password                     Password for password spraying   
  
  -w, --wordlist                     Wordlist file               
  
  -V, --check_version                Check SSH version
  
  -b, --bruteforce                   Execute bruteforce attack
  
  -s, --password_spray               Execute password spraying attack

