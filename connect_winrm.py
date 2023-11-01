from lib.WinRM_Python import WinRmPython


class TestWinRM:

    def __init__(self, host_ip, username, password):
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.winrm_python = WinRmPython(self.host_ip, self.username, self.password)

    def main(self):
        file_path = "/home/devuser/abc"
        exit_status, out, error = self.winrm_python.execute_command(f"cat {file_path}")
        print(exit_status, out, error)
        #print(self.winrm_python.check_file(file_path))
        print(self.winrm_python.download_file(file_path, "D:\/"))
        return True, "Success"


if __name__ == "__main__":
    status, message = TestWinRM("localhost", "test", "test").main()
