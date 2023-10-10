import datetime

import paramiko
import logging

# SSH connection parameters
server_ip_address = '192.168.151.234'
ssh_port = 22
ssh_username = 'yves'
ssh_password = 'yves'  # or use a private key
iptables_rules_file_path='iptables_rules.txt'
# Path to the log file on the client machine
log_file_path = f'/home/{ssh_username}/iptables.log'

# config log
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='client.log')

def read_iptables_rules(path):
    try:
        # Open the file in read mode
        with open(iptables_rules_file_path, 'r') as file:
            # Read the content of the file
            content = file.readlines()
        return content
    except FileNotFoundError:
        # Handle the exception if the file is not found
        logging.error("The file was not found.")
    except IOError as e:
        # Handle other exceptions related to file reading
        logging.error(f"An error occurred while reading the file: {e}")
    except Exception as e:
        # Handle all other unexpected exceptions
        logging.error(f"An exception occurred: {e}")
def main():
    try:
        # Create a Paramiko SSHClient instance
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        ssh.connect(server_ip_address, ssh_port, ssh_username, ssh_password)

        # Execute the iptables command from the file and redirect the output to the log file
        #stdin, stdout, stderr = ssh.exec_command("ls -lah" + f' > {log_file_path} 2>&1')

        for c in read_iptables_rules(iptables_rules_file_path):
            command = f"sudo {c.strip()}  >> {log_file_path}"
            logging.debug("[IPTABLES RULE]# " + command)

            # date format
            t = datetime.datetime.now()
            ssh.exec_command(f"echo [{t.date()} {t.time()}]: {command} >> {log_file_path} 2>&1")
            stdin, stdout, stderr = ssh.exec_command(command)

            # Wait for the command to complete
            exit_status = stdout.channel.recv_exit_status()

            output = stdout.read().decode('utf-8')
            errors = stderr.read().decode('utf-8')


            # script exec verification
            if exit_status != 0:
                logging.error(errors)
            else:
                logging.info('-------- SUCCED')
            ssh.exec_command(f"echo {'-------- SUCCED' if exit_status == 0 else '-------- ERROR'} "
                             f">> {log_file_path} 2>&1")

    except paramiko.AuthenticationException:
        logging.error('SSH Auth failed')
    except paramiko.SSHException as e:
        logging.error(f'SSH Error : {e}')
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        # Close the SSH connection
        ssh.close()

if __name__ == '__main__':
    main()