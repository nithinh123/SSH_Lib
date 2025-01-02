from pypsrp.client import Client
from pypsrp.exceptions import AuthenticationError, WinRMTransportError, WinRMError


class WinRmPython:
    """
    A class to execute PowerShell scripts on a remote Windows server using pypsrp.
    """

    def __init__(self, server, username, password, auth="ntlm", ssl=False):
        """
        Initializes the RemotePowerShellExecutor with server details, credentials, and authentication method.

        Parameters:
        server (str): The IP address or hostname of the remote server.
        username (str): The username for authentication.
        password (str): The password for authentication.
        auth (str): The authentication method ('ntlm', 'kerberos', or 'basic').
        ssl (bool): Whether to use SSL for the connection.
        """
        self.server = server
        self.username = username
        self.password = password
        self.auth = auth
        self.ssl = ssl
        self.client = None

    def establish_connection(self):
        """
        Establishes a PSRP connection to the remote server.
        """
        try:
            self.client = Client(
                self.server,
                username=self.username,
                password=self.password,
                auth=self.auth,
                ssl=self.ssl
            )
            print(f"Successfully established connection to {self.server} using {self.auth} authentication")
        except AuthenticationError:
            print("Authentication Error. Please check the credentials provided.")
        except WinRMTransportError:
            print("WinRM Transport Error. Please check the connection and server configuration.")
        except WinRMError:
            print("WinRM Error occurred.")
        except AuthenticationError:
            print("Authentication Error. Please check the credentials provided.")
        except WinRMTransportError:
            print("WinRM Transport Error. Please check the connection and server configuration.")
        except WinRMError as e:
            print("WinRM Error occurred. Error: ", str(e))
        except Exception as e:
            print(self.server, " - An unexpected error occurred while connecting to the server.")
            print("Exception: ", str(e))

    def execute_script(self, script):
        """
        Executes a PowerShell script on the remote server.

        Parameters:
        script (str): The PowerShell script content.

        Returns:
        dict: A dictionary containing the script's output and status.
        """
        if self.client is None:
            raise RuntimeError("Connection not established. Call 'establish_connection' first.")

        try:
            # Execute the PowerShell script
            output, streams, had_errors = self.client.execute_ps(script)

            if had_errors:
                error_message = "\n".join([str(err) for err in streams.error])
                return {
                    "status": "error",
                    "error_message": error_message
                }
            else:
                return {
                    "status": "success",
                    "output": output
                }
        except Exception as e:
            raise RuntimeError(f"Error executing script: {e}") from e

    @staticmethod
    def read_script(file_path, **kwargs):
        """
        Reads a PowerShell script from a file and optionally formats it with parameters.

        Parameters:
        file_path (str): The path to the PowerShell script file.
        kwargs (dict): Parameters to format the script with.

        Returns:
        str: The content of the PowerShell script, formatted with the provided parameters.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                script = file.read()
                if kwargs:
                    script = script.format(**kwargs)
                return script
        except OSError as e:
            raise RuntimeError(f"Error reading script file: {e}") from e
