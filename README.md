# ConfDes: Cisco Interface Description Updater

**ConfDes** is a Python script designed to automate the process of configuring interface descriptions on Cisco C1300 series switches based on **CDP (Cisco Discovery Protocol)** information.

This project was initiated to solve the challenge of manually configuring over 180 Cisco C1300 switches connected to more than 2,000 Access Points. By automatically pulling CDP data, ConfDes translates it into configuration commands, significantly reducing the time and effort required for network administration.

---

### Key Features

* **SSH Secure Connection:** Establishes secure SSH connections to Cisco C1300 switches, handling a two-level login process (user and enable mode).
* **Automated Configuration:** Analyzes `show cdp neighbor` output to generate and apply port descriptions automatically.
* **Flexible Command Execution:** Executes predefined commands in both `enable` and `config` modes.
* **Comprehensive Logging:** Records all commands and their outputs to a `HOSTNAME.txt` file for easy review and auditing.
* **Modularity:** The codebase is structured into a library (`config_des.py`), making it easy to extend and integrate into other projects.

---

### Installation & Usage

This project requires **Python 3.x** and the `paramiko` library.

#### 1. Preparation

* **`host_list.txt`**: Create this file to list the hostnames and IP addresses of the switches. Each line should be in the format `HOSTNAME,IP_ADDRESS`.
    * **Example:**
        ```
        SWITCH-001,192.168.1.10
        SWITCH-002,192.168.1.11
        ```

#### 2. Running the Script

1.  Open your terminal or command prompt.
2.  Execute the script with the following command:
    ```bash
    python main.py
    ```
3.  You will be prompted to enter a **Username** and **Password** for the switch logins.
4.  The script will then process each switch listed in `host_list.txt`, and a detailed log of its operations will be saved to `logs.txt`.

---

#### Breakdown of `config_des.py`

This library contains several key functions:

* `ssh_connect()`: Handles the SSH connection process.
* `run_command()`: Executes commands in `enable` mode.
* `config_command()`: Executes commands in `config` mode.
* `save_config()`: Commits the configuration changes to the device.
* `save_logs_file()`: Writes all command output to `logs.txt`.
* `edit_config()`: Parses `show cdp neighbor` output to create config commands.
* `get_host_list()`: Reads switch information from `host_list.txt`.

---

### Contribution

**Me, Myself, and I.**
