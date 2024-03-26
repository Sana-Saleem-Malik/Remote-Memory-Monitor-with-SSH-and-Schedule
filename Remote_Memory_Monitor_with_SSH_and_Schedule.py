import schedule
import time
import paramiko
from datetime import datetime

def gather_memory_info(hostname, username, password):
    try:
        # Current date and time
        current_date = datetime.today().strftime("%B %d %Y")
        current_time = datetime.now().strftime("%I:%M:%S %p")

        # Establish SSH connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=hostname, username=username, password=password)

        # Commands to retrieve memory information
        available_memory_cmd = "free -g | grep Mem | awk '{print $7}'"
        total_memory_cmd = "free -g | grep Mem | awk '{print $2}'"
        used_memory_cmd = "free -g | grep Mem | awk '{print $3}'"

        # Execute commands on the remote server
        stdin, stdout, stderr = client.exec_command(available_memory_cmd)
        available_memory = stdout.read().decode().strip()
        stdin, stdout, stderr = client.exec_command(total_memory_cmd)
        total_memory = stdout.read().decode().strip()
        stdin, stdout, stderr = client.exec_command(used_memory_cmd)
        used_memory = stdout.read().decode().strip()

        # Format memory information
        memory_details = f"""Task:
        Memory Detail:
        {current_date} {current_time} and Memory details are as follows:
        Available Memory: {available_memory} GB
        Total Memory: {total_memory} GB
        Used Memory: {used_memory} GB"""

        # Write memory information to a text file
        with client.open_sftp() as sftp:
            sftp.chdir("/home/osboxes/lec51")
            filename = f"Memory_detail_{datetime.now().strftime('%B_%d_%Y_%I:%M:%S_%p')}.txt"
            with sftp.open(filename, 'w') as file:
                file.write(memory_details)

        # Close SSH connection
        client.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def schedule_memory_report(hostname, username, password):
    # Schedule memory report task to run daily
    job1 = schedule.every().minute.do(gather_memory_info, hostname, username, password)

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)

# Example usage:
schedule_memory_report("192.168.100.2", "admin", "password123")
