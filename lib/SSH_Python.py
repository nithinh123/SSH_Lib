import paramiko
import os
import socket
import time
import requests
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

Fail = False
Pass = True


class SSHPython:
    """
        This class will do multiple functions in remote systems through ssh
    """

    def __init__(self, host_ip, username, password):
        self.client = None
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.connect_host()

    def execute_command(self, command, timeout=600, exit_code_check=False, print_commands=False, print_error_msg=False):
        """
            Execute a command on the remote host. Return a tuple containing
            a boolean status and two strings, the first containing stdout
            and the second containing stderr from the command
        """
        ssh_output = None
        ssh_error = None
        result_flag = Pass
        cmd_exit_code = 1
        try:
            if self.client:
                time.sleep(1)
                if print_commands:
                    print("Executing command --> ", command)
                stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
                ssh_output = stdout.read().decode('UTF-8').strip("\n")
                ssh_error = stderr.read().decode('UTF-8').strip("\n")
                if exit_code_check:
                    cmd_exit_code = stdout.channel.recv_exit_status()
                if cmd_exit_code != 0 and exit_code_check and print_error_msg:
                    print("Problem occurred while running command:" + command + ssh_error)
                    result_flag = Fail
                elif ssh_error and print_error_msg:
                    print("Problem occurred while running command:" + command + ssh_error)
                    result_flag = Fail
                if print_commands:
                    print("Command execution completed successfully", command)
            else:
                print("Could not establish SSH connection")
        except socket.timeout:
            print("Command timed out.", command)
        except paramiko.SSHException:
            print("Failed to execute the command!", command)
            result_flag = Fail
        except Exception as e:
            print("Failed to execute the command!", command)
            print("Exception:", e)
            result_flag = Fail
        return result_flag, ssh_output, ssh_error

    def upload_file(self, local_file_path, remote_file_path):
        """
            This method uploads the file to remote server
        """
        result_flag = Pass
        try:
            if self.client:
                ftp_client = self.client.open_sftp()
                ftp_client.put(local_file_path, remote_file_path)
                ftp_client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = Fail
        except Exception as e:
            print("Unable to upload the file to remote server", remote_file_path)
            print("Exception:", e)
        return result_flag

    def download_file(self, remote_file_path, local_file_path):
        """
            This method download the file from remote server
        """
        result_flag = Pass
        try:
            if self.client:
                ftp_client = self.client.open_sftp()
                ftp_client.get(remote_file_path, local_file_path)
                ftp_client.close()
            else:
                print("Could not establish SSH connection")
                result_flag = Fail
        except Exception as e:
            print("Unable to download the file from remote server", remote_file_path)
            print("Exception:", e)
        return result_flag

    def connect_host(self):
        """
            Login to the remote server
        """
        result_flag = Pass
        if self.host_ip is None and self.username is None and self.password is None:
            return "Skipping client creation", True
        try:
            print("Establishing ssh connection.....")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(hostname=self.host_ip, port=22, username=self.username, password=self.password,
                                timeout=20, allow_agent=False, look_for_keys=False)
            print(self.host_ip, " - Connected to the server")
        except paramiko.AuthenticationException:
            print(self.host_ip, " - Authentication failed, please verify your credentials")
            result_flag = Fail
            self.client = None
        except paramiko.SSHException as ssh_exception:
            print(self.host_ip, " - Could not establish SSH connection:", str(ssh_exception))
            result_flag = Fail
            self.client = None
        except socket.timeout as socket_timeout:
            print(self.host_ip, " - Connection timed out")
            print("Exception: ", str(socket_timeout))
            result_flag = Fail
            self.client = None
        except Exception as e:
            print(self.host_ip, " - Exception in connecting to the server")
            print("Exception: ", str(e))
            result_flag = Fail
            self.client = None
        return self.client, result_flag

    def check_file(self, file_path, data_type="File"):
        """
            This method checks if a file or directory exists

        """
        try:
            if self.client:
                if data_type == "File":
                    status, ssh_output, ssh_error = self.execute_command(f'test -f {file_path}',
                                                                         10, True)
                else:
                    status, ssh_output, ssh_error = self.execute_command(f'test -d {file_path}',
                                                                         10, True)
            else:
                print("Could not establish SSH connection")
                status = Fail
        except Exception as e:
            print("Exception: ", str(e))
            status = Fail
        return status

    def put_all(self, localpath, remotepath):
        """
            Copying directory recursively to remote location
        """
        try:
            sftp = self.client.open_sftp()
            os.chdir(os.path.split(localpath)[0])
            parent = os.path.split(localpath)[1]
            for walker in os.walk(parent):
                try:
                    remote_path = os.path.join(remotepath, walker[0])
                    remote_path = remote_path.replace("\\", "/")
                    sftp.mkdir(remote_path)
                    sftp.cwd(remote_path)
                except Exception:
                    pass
                for file in walker[2]:
                    file_path = os.path.join(localpath, file)
                    remote_file_path = remotepath + "/" + file.replace("\\", "/")
                    print(file_path, remote_file_path)
                    try:
                        sftp.put(file_path, remote_file_path)
                    except Exception:
                        continue
                for file in os.listdir(os.path.join(os.getcwd(), parent, walker[1][0])):
                    file_path = os.path.join(os.getcwd(), parent, walker[1][0], file)
                    remote_file_path = remotepath + "/" + file.replace("\\", "/")
                    print(file_path, remote_file_path)
                    try:
                        sftp.put(file_path, remote_file_path)
                    except Exception:
                        continue
                sftp.chdir(remotepath)
        except Exception as e:
            print("Exception: ", str(e))

    def get_channel(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host_ip, 22, self.username, self.password)
            return ssh.invoke_shell()
        except Exception as e:
            print(self.get_stamp() + "Exception in connecting to host")
            print("Exception: ", str(e))

    def wait_for_channel(self):
        channel_ready_status = True
        global channel, channel_data
        try:
            while channel_ready_status:
                if channel.recv_ready():
                    print(self.get_stamp() + "Getting initial connection information")
                    channel_data += str(channel.recv(9999))
                    time.sleep(5)
                    print(self.get_stamp() + "Channel is ready")
                    channel_ready_status = False
                else:
                    time.sleep(5)
                    continue
        except Exception as e:
            print("Exception in getting channel back")
            print("Exception: ", str(e))
        return channel_ready_status

    def send_cmd(self, cmd, islist=False):
        global channel, channel_data
        try:
            if islist and type(cmd) is not None:
                for command in cmd:
                    channel_data = ""
                    channel.send(command)
                    channel.send("\n")
                    time.sleep(1)
                    channel_data = str(channel.recv(9999))
            elif cmd != "":
                channel.send(cmd)
                channel.sent("\n")
                time.sleep(1)
                channel_data = str(channel.recv(9999))
        except Exception as e:
            print(f"Exception in {cmd} execution")
            print("Exception: ", str(e))
        return channel_data

    @staticmethod
    def get_stamp():
        return str(datetime.now())
