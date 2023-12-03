import time

import paramiko


class Connector:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.__ssh_client = paramiko.SSHClient()
        self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh_client.connect(
            hostname=hostname,
            username=username,
            password=password,
            port=22
        )
        self.shell = self.__ssh_client.invoke_shell()

    def __del__(self):
        if hasattr(self, 'client') and self.__ssh_client is not None:
            self.__ssh_client.close()

    def send_shell_command(self, command, user_input=""):

        self.shell.send(command + '\n')
        time.sleep(2)
        response = self.shell.recv(10000)

        text = response.decode("utf-8")

        if len(user_input) > 0:
            self.shell.send(user_input)
            time.sleep(2)
            response = self.shell.recv(10000)

            text = response.decode("utf-8")

        return text

    def send_exec_command(self, command):
        self.__ssh_client.exec_command(command)
        stdin, stdout, stderr = self.__ssh_client.exec_command(command + "\n")
        time.sleep(1)
        return stdout.read().decode()