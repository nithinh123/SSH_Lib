import pypsrp.exceptions
from pypsrp.client import Client

Fail = False
Pass = True


class WinRmPython:

    def __init__(self, host_ip, username, password):
        self.client = None
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.connect_host()

    def connect_host(self):
        try:
            print("Establishing WinRM connection.....")
            self.client = Client(server=self.host_ip, username=self.username, password=self.password)
        except pypsrp.exceptions.AuthenticationError:
            print("Authentication Error. Please check the credentails provided")
        except pypsrp.exceptions.WinRMTransportError:
            print("WinRMTransportError")
        except pypsrp.exceptions.WinRMError:
            print("WinRMError")
        except Exception as e:
            print(self.host_ip, " - Exception in connecting to the server")
            print("Exception: ", str(e))
            self.client = None
        return self.client

    def execute_command(self, command):
        stdout, stderr, rc = self.client.execute_cmd(command)
        stdout, stderr, rc = self.client.execute_cmd("powershell.exe gci $pwd")
        sanitised_stderr = self.client.sanitise_clixml(stderr)

    def execute_ps_script(self, script_path):
        # execute a PowerShell script
        output, streams, had_errors = self.client.execute_ps('''$path = "%s"
        if (Test-Path -Path $path) {
            Remove-Item -Path $path -Force -Recurse
            }
            New-Item -Path $path -ItemType Directory''' % script_path)
        output, streams, had_errors = self.client.execute_ps("New-Item -Path C:\\temp\\folder -ItemType Directory")

    def upload_file(self, local_path, remote_path):
        # copy a file from the local host to the remote host
        self.client.copy("~/file.txt", "C:\\temp\\file.txt")

    def download_file(self, remote_path, local_path):
        # fetch a file from the remote host to the local host
        self.client.fetch("C:\\temp\\file.txt", "~/file.txt")
