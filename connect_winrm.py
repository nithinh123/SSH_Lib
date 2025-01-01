from lib.WinRM_Python import WinRmPython


if __name__ == "__main__":
    # Replace with your server details and credentials
    server = "hostname"  # Replace with the server's IP or hostname
    username = "devuser"  # Replace with the username
    password = "Password"  # Replace with the password
    script_path = "D:/abc/script.ps1"  # Replace with the path to your PowerShell script file
    auth_method = "ntlm"  # Options: 'ntlm', 'kerberos', 'basic'
    use_ssl = False  # Set to True if SSL is required

    try:
        # Initialize the class with authentication and SSL options
        executor = WinRmPython(server, username, password, auth=auth_method, ssl=use_ssl)

        # Establish connection
        executor.establish_connection()

        # Read the PowerShell script
        script_content = executor.read_script(script_path)

        # Execute the PowerShell script
        result = executor.execute_script(script_content)

        # Output the result
        if result["status"] == "success":
            print("Script executed successfully!")
            print("Output:")
            print(result["output"])
        else:
            print("Error executing script!")
            print("Error message:")
            print(result["error_message"])
    except Exception as e:
        print(f"An error occurred: {e}")
