import socket
import sys
import threading
import traceback

import paramiko

from config_manager import ServerConfig
from ssh_client import SshClient


class SshServer(paramiko.ServerInterface):

    def __init__(self, ssh_client: SshClient, config: ServerConfig):
        # paramiko.util.log_to_file("server.log")
        self.event = threading.Event()
        self.ssh_client = ssh_client
        self.config = config

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    def handle_cmd(self, channel, command):
        stdout = channel.makefile('wb')
        stderr = channel.makefile_stderr('wb')
        command = command.decode()
        out_msg, error_msg = self.ssh_client.run_cmd(command=command)
        stdout.write(out_msg)
        stderr.write(error_msg)
        stdout.flush()
        stderr.flush()
        stdout.close()
        stderr.close()
        channel.send_exit_status(0)
        channel.event.set()
        channel.shutdown_write()
        channel.close()

    def check_channel_exec_request(self, channel, command):
        t = threading.Thread(target=self.handle_cmd, args=(channel, command))
        t.start()
        return True

    def run_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.config.ip, self.config.port))
            host_key = paramiko.RSAKey.generate(1024) if self.config.key_path == '' else paramiko.RSAKey(
                filename=self.config.key_path)
            print('***SSH PROXY SERVER {}:{} STARTED***'.format(self.config.ip, self.config.port))
        except Exception as e:
            traceback.print_exc()
            sys.exit(1)
        while True:
            try:
                sock.listen(100)
                client, addr = sock.accept()
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

            t = paramiko.Transport(client)
            try:
                t.load_server_moduli()
            except:
                print("(Failed to load moduli -- gex will be unsupported.)")
                raise

            t.add_server_key(host_key)
            try:
                t.start_server(server=self)
            except Exception as e:
                print("*** SSH negotiation failed\n{}".format(e))

            try:
                channel = t.accept(5)
            except Exception as e:
                print("*** Open channel failed\n{}".format(e))
