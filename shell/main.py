# Standard library
import os
import sys
import json
import shlex
import time
import socket
import shutil
import pprint
import datetime
import subprocess
import webbrowser
from collections import deque
from pathlib import Path

# Local
from errorclass import ErrorCode
from toolbox import tools

class ansi_color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RED = '\033[91m'
    RESET = '\033[0m'

#global history double ended queue
history = deque(maxlen=35)

#error handler
def error(message):
    if isinstance(message, ErrorCode):
        message = message.value
    print(f"{ansi_color.RED}{message}{ansi_color.RESET}")
    return

#directory access
def shell_directory():
    script_directory = Path(__file__).parent
    return script_directory

#reading JSON of socketErrno
def socketErrno_reader():
    script_directory = shell_directory()
    file_path = script_directory / 'socketErrno.json'
    with file_path.open('r') as file:
        sock_data = json.load(file)
        return sock_data

#port valid range
def valid_range(PORT: int) -> bool:
    maximum_port = 65535
    return 1 <= PORT <= maximum_port

#initialize sockets
def socket_initialize(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        status = sock.connect_ex((HOST, PORT))
        return status

#scan results
def scan_initialize(PORT, status, sock_data):
    if status == 0:
        print(f"Port >> {PORT} >> {ansi_color.GREEN}{sock_data[str(status)]}{ansi_color.RESET}")
    if status > 0: 
        print(f"Port >> {PORT} >> {ansi_color.RED}{sock_data[str(status)]}{ansi_color.RESET}")
    return

#connectivity tester and port scanner   
def connection_portal(command, command_split):
    sock_data = socketErrno_reader()
    match len(command_split):
        case 4:
            if command_split[1] == 'range':
                print(f"{ansi_color.GREEN}SCAN from {command_split[2]} To {command_split[3]}{ansi_color.RESET}")
                scanrange_min = int(command_split[2])
                scanrange_max = int(command_split[3]) + 1
                for port_iterator in range(scanrange_min, scanrange_max):
                    HOST = '127.0.0.1' 
                    PORT = int(port_iterator)

                    if not valid_range(PORT):
                        error(ErrorCode.PortNotInRange)
                        return
                    
                    status = socket_initialize(HOST, PORT)
                    try: scan_initialize(PORT, status, sock_data)  
                    except KeyError: 
                        error(ErrorCode.ConnectionFailed)
                        break
                return
            else: 
                error(ErrorCode.ConnectionFailed)
                return

        case 3:
            try: 
                HOST = socket.gethostbyname(str(command_split[1]))
            except socket.gaierror: 
                error(ErrorCode.HostnameNotFound)
                return
        
            PORT = int(command_split[2])
            if not valid_range(PORT):
                error(ErrorCode.PortNotInRange)
                return
            
            print(f"{ansi_color.GREEN}Connnecting To {HOST} From {PORT}{ansi_color.RESET}")
            status = socket_initialize(HOST, PORT)
            scan_initialize(PORT, status, sock_data)  
            return
            
        case _:
            error(ErrorCode.ConnectionFailed)
            return

#executing file
def execute_file(command, command_split):
    if len(command_split) < 2:
        error(ErrorCode.InvalidArguments)
        return
    
    execute_path = shutil.which(command_split[1])
    if execute_path is None:
        error(ErrorCode.FileNotFound)
        return
    
    if os.access(str(execute_path), os.X_OK):
        print(f"{ansi_color.GREEN}Opening File{ansi_color.RESET} >> ({execute_path})")
        try:
            subprocess.run(execute_path, check=True, shell=False)
            return
        except subprocess.CalledProcessError:
            error(ErrorCode.UnableToExecuteFile)
            return
    else: 
        error(ErrorCode.UnableToExecuteFile)
        return

#website opener
def open_website(command, command_split):      
    if len(command_split) == 2:
        url = command_split[1]
        if not url.startswith(('http://', 'https://')):     
            url = "https://" + url
        webbrowser.open(url)
        return
    else: 
        error(ErrorCode.WebsiteNotFound)
        return
    
#environment variables   
def environ_print(command, command_split):
    if len(command_split) == 1:
        envar = os.environ
        pprint.pprint(dict(envar), width=5, indent=5) 
        return
    else: 
        error(ErrorCode.InvalidArguments)
        return

#check if file is in the system
def file_check(type_file) -> bool:
    if type_file is not None:
        return os.access(type_file, os.X_OK)
    
#builtin commands checker
def type_command(command, command_split):
    match len(command_split):
        case 2:
            type_file = shutil.which(command_split[1])
            if command_split[1] in commands:
                print(f"{command_split[1]} >> {commands.get(command_split[1])}")
                return

            if file_check(type_file):
                print(f"{command_split[1]} >> {type_file}")
                return 
            
            else: 
                error(ErrorCode.CommandNotFound)
                return
        case _: 
            error(ErrorCode.InvalidArguments)
            return

#change current working directory
def change_directory(command, command_split):
    script_directory = shell_directory()

    if len(command_split) > 1:
        directory = str(command_split[1])

        if command_split[1] == 'reset':
            os.chdir(script_directory)
            return
        
        if not os.path.exists(directory):
            error(ErrorCode.PathNotFound)
            return
        
        if not os.path.isdir(directory):
            error(ErrorCode.DirectoryNotFound)
            return

        try: 
            os.chdir(str(directory))
            return
        
        except FileNotFoundError: 
            error(ErrorCode.FileNotFound)
            return
    else: 
        error(ErrorCode.FileNotFound)
        return

#external tool wrappers 
def external_tools(command, command_split):
    if command_split[0] in tools:
        try: 
            subprocess.run(command_split, shell=False, check=True)
            return
        
        except subprocess.CalledProcessError: 
            error(ErrorCode.SubprocessError)
            return
    else:
        error(ErrorCode.CommandNotFound)
        return

#access history deque
def modify_history(command, command_split):  
    if len(command_split) == 1:
        print(f"{ansi_color.GREEN} >> Command History{ansi_color.RESET}")
        for element in history:
            print(f">> {element}")
        return     
    
    if len(command_split) == 2:
        match command_split[1]:
            case 'clear':
                history.clear()
                return
            case _: 
                error(ErrorCode.InvalidArguments)
                return
    else: 
        error(ErrorCode.InvalidArguments)
        return

commands = {
    "exit": lambda command, command_split: sys.exit(0),
    "python": lambda command, command_split: print(sys.version),
    "echo": lambda command, command_split: print(*command_split[1:]),
    "com": lambda command, command_split: pprint.pprint(dict(commands), width = 5),
    "git": external_tools,
    "curl": external_tools,
    "type": type_command,
    "web": open_website,
    "env": environ_print,
    "file": execute_file,
    "change": change_directory,
    "con": connection_portal,
    "history": modify_history
}

#executing commands
def command_execute(current_directory):
    try:
        max_token = 63
        command = input()
        if command == '': return
        try: command_split = shlex.split(command) 

        except ValueError: 
            error(ErrorCode.ValueErrorInput)
            return
        
        for element in range(len(command_split)):
            if len(command_split[element]) >= max_token:
                error(ErrorCode.MaxTokenExceeded)
                return
    
        if command_split[0] in commands:
            start_time = time.time()
            execute = commands.get(command_split[0])
            execute(command, command_split)
            end_time = time.time()
            history.append(f"{command} - PERFORMANCE {end_time - start_time:.5f}")
        
        else: 
            error(ErrorCode.CommandNotFound)
            return

    except KeyboardInterrupt: 
        error(ErrorCode.KBInterrupt)
        return
    
def main():
    try:
        print(f">> {ansi_color.GREEN}Connecting{ansi_color.RESET} / <Turn Firewall Off>")
        HOST, PORT = '1.1.1.1', 443
        with socket.create_connection((HOST, PORT), timeout = 1.0): 
            print(f"Initial Network Status >> {ansi_color.GREEN}Online{ansi_color.RESET}")
    
    except OSError:
        print(f"Initial Network Status >> {ansi_color.RED}Offline{ansi_color.RESET}")

    except KeyboardInterrupt: sys.exit(0)

    date = datetime.datetime.now()
    print(f"{ansi_color.PURPLE}tt-shell [{sys.argv[0]}]{ansi_color.RESET} / {ansi_color.BLUE}{date}{ansi_color.RESET}")
    while True:
        current_directory = os.getcwd()
        sys.stdout.write(f"[{current_directory}]{ansi_color.GREEN} >> {ansi_color.RESET}")
        command_execute(current_directory)

if __name__ == "__main__":
    main()