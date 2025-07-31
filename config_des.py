import paramiko
import time
from pathlib import Path
import re 
import logging

# Location log file.
logfile = Path(__file__).parent / "logs.txt"

# Create main logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Log format.
formatter = logging.Formatter(
    fmt="{asctime}   <{levelname}>   {message}",
    style="{",
    datefmt="%Y-%m-%d  %H:%M:%S"
)

# Create FileHandler.
file_handler = logging.FileHandler(logfile, mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)

# Create StreamHandler for console.
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add handler.
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def ssh_connect(host, username, password):
    try:
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            connection.connect(host,username=username,timeout=30)
            channel = connection.invoke_shell()
        except:
            try:
                connection.get_transport().auth_none(username)
                channel = connection.invoke_shell()
                channel.send(f"{username}\n")
                time.sleep(0.5)
                channel.send(f"{password}\n")
                time.sleep(0.5)  
                channel.send(f"\n")
                time.sleep(0.5)  
                output = channel.recv(1000).decode('utf-8').strip().split('\n')[-1]

                if output.endswith('#'):
                    hostname = str(output.replace("#","").strip())
                    logging.info(f"Connected to {hostname} successfully.")
                    
                    hostname = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',hostname)                    
                    return channel,hostname

                else :
                    logging.error(f"Connected to {host}. Login authentication failed.")
                    return None
                
            except Exception as e:
                logging.error(f"Failed to connect to {host} . | {e}")

                return None  
            
        
    
    except Exception as e:
        logging.error(f"Failed to connect to {host} .| {e}")
        return None 

def run_command(connection, command):  
        channel = connection
        buffer = ""

        try:
            channel.send(command + '\n')   
            while not buffer.strip().endswith(("#", ">")):
                if channel.recv_ready():
                    recv = channel.recv(65535).decode('utf-8')
                    buffer += recv
        except Exception as e:
            logging.error(f"Can not run '{command}' | {e}")
        buffer = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',buffer)
        return buffer

def config_command(channel, commands):
    output = ""
    try:
        channel.send('configure terminal\n')
        for command in commands:
            channel.send(command + '\n')
            time.sleep(1)
            while not output.strip().endswith(("#")):
                if channel.recv_ready():
                    recv = channel.recv(65535).decode('utf-8')
                    output += recv
        channel.send('end\n')
        logging.info(f"Configuration commands executed successfully.")

    except Exception as e:
        logging.error(f"Invalid config. | {e}")
    output = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',output)
    return output

def save_config(channel):
    buffer = ""
    
    try:
        channel.send('wr\n')
        while not buffer.strip().endswith(("#", ">")):
                if channel.recv_ready():
                    recv = channel.recv(65535).decode('utf-8')
                    buffer += recv
                    if buffer.strip().endswith("?"):
                        channel.send("Y\n")
                        buffer += channel.recv(65535).decode('utf-8')

                    time.sleep(0.1)
        logging.info("Saved configuration successfully.")
        buffer = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]','',buffer)
        return buffer
    
    except Exception as e:
        logging.error(f"Cannot save the configuration. | {e}")

def save_logs_file(filname,logs):
    full_path = Path(__file__).parent / "logs" / f"{filname}.txt"
    
    try:
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(logs)
        logging.info(f"Saved logs '{filname}' successfully.")
        return full_path
    
    except Exception as e:
        logging.error(f"Failed to save logs to {full_path}. | {e}")
        return None 
    
def edit_config(show_cdp_output):
    config_lines = []
    try:
        for line in show_cdp_output.strip().splitlines():
            if "AP" in line and "gi" in line:
                parts = line.split()
                if len(parts) < 2:
                    continue
                ap_name = parts[0].strip()
                interface = parts[1].strip()
                config_lines.append(f"interface {interface}")
                config_lines.append(f"description Connected_{ap_name}")
        logging.info('Configuration applied successfully.')
        
    except Exception as e:
        logging.error(f"Cannot create command config. | {e}")


    return config_lines

def get_host_list(file_host):
    host_list = []
    ip_list =[]

    try:
        with file_host.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if "," in line:
                if len(line) < 2:
                    continue
                host, ip = line.strip().split(',')
                host_list.append(host.strip())
                ip_list.append(ip.strip())
        return host_list, ip_list
    except Exception as e:
        logging.error(f"Cannot read file '{file_host}'. | {e}")
        return [], []
