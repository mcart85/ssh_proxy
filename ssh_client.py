from typing import Tuple
from paramiko.client import SSHClient
from config_manager import ClientConfig
import paramiko

from custom_response import CustomResponse
from logger import ResponseLogger


class SshClient:
    def __init__(self, client_config: ClientConfig, logger: ResponseLogger, custom_response: CustomResponse):
        self.credentials = client_config
        self.logger = logger
        self.custom_response = custom_response
        self.session: SSHClient = None

    def run_cmd(self, command: str) -> Tuple[bytes, bytes]:
        is_custom = False
        if self.custom_response.has_custom_response(command=command):
            is_custom = True
            output, error = self.custom_response.get_custom_response(command=command)
        else:
            ssh = self.get_session()
            _, out, err = ssh.exec_command(command)
            error = err.read()
            output = out.read()
        self.logger.log_out(is_custom=is_custom, command=command, out=output.decode())
        self.logger.log_error(is_custom=is_custom, command=command, err=error.decode())
        return output, error

    def get_session(self) -> SSHClient:
        if self.session is None:
            self.session = self.create_session()
        elif not self.session.get_transport().is_alive():
            print('Session is Dead. Create New session.')
            self.session = self.create_session()
        return self.session

    def create_session(self) -> SSHClient:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cred = self.credentials
        ssh.connect(hostname=cred.hostname,
                    username=cred.username,
                    password=cred.password,
                    port=cred.port)
        return ssh
