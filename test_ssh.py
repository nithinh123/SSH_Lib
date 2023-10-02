from lib.SSH_Python import SSHPython


class TestSSH:

    def __init__(self, host_ip, username, password):
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.ssh_python = SSHPython(self.host_ip, self.username, self.password)

    def main(self):
        file_path = "/home/devuser/abc"
        exit_status, out, error = self.ssh_python.execute_command(f"cat {file_path}")
        print(exit_status, out, error)
        print(self.ssh_python.check_file(file_path))
        print(self.ssh_python.download_file(file_path, "D:\/"))
        return True, "Success"


if __name__ == "__main__":
    status, message = TestSSH("localhost", "devuser", "12345").main()
