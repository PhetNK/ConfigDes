import config_des
from pathlib import Path

#Get host and ip from file.
file_name = Path(__file__).parent / "list_host.txt"
host_list,ip_list = config_des.get_host_list(file_name)

#Enter username and password for all hosts.
username = input("Enter Username: ")
password = input("Enter Password: ")


for ip in ip_list :
    try:
        #SSH connect to switch
        session,hostname = config_des.ssh_connect(ip, username, password)

        #Get dcp_teble
        cdp_table = config_des.run_command(session,"show cdp nei | include AP")

        #Edit config
        new_config = config_des.edit_config(cdp_table)

        #Config interface description.
        config_des.config_command(session,new_config)
        #Commande for save logs.
        command_log = [
        "terminal datadump",
        "show cdp neighbors | include AP",
        "show interface description",
        "terminal no datadump"
        ]

        #Get logs file.
        log_output = ""
        for command in command_log:
            log_output += config_des.run_command(session, command)
        log_save = config_des.save_config(session)

        #Save to text file.
        config_des.save_logs_file(hostname,log_output+log_save)

    except:
        print(f"[Error] Invalid host configuration. IP address: {ip}")
        if session.get_transport().is_active():
            session.close()
        continue
