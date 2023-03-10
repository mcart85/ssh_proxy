import configparser
import os


class ClientConfig:
    def __init__(self, host, username, password, port):
        self.hostname = host
        self.username = username
        self.password = password
        self.port = port


class ServerConfig:
    def __init__(self, ip: str, port: int, key_path: str):
        self.ip = ip
        self.port = port
        self.key_path = key_path


class LogTags:
    def __init__(self):
        self.command_tag = None
        self.start_tag = None
        self.end_tag = None


class LogOutTags(LogTags):
    def __init__(self):
        self.command_tag = "Command => "
        self.start_tag = "Output =>\n"
        self.end_tag = "<= Output end\n"


class LogErrTags(LogTags):
    def __init__(self):
        self.command_tag = "Command => "
        self.start_tag = "Error =>\n"
        self.end_tag = "<= Error end\n"


class CustomResponseConfig:
    def __init__(self, out_file_path: str, err_file_path: str, log_out_tags: LogTags, log_err_tags: LogTags,
                 pause: float):
        self.out_path = out_file_path
        self.err_path = err_file_path
        self.log_out_tags = log_out_tags
        self.log_err_tags = log_err_tags
        self.pause = pause


class ConfigManager:
    def __init__(self, config_ini_path: str = None):
        self.client_config = None
        self.server_config = None
        self.custom_response_config = None
        self.log_out_tags = LogOutTags()
        self.log_err_tags = LogErrTags()
        self.read_configuration(config_ini_path=config_ini_path)

    def read_configuration(self, config_ini_path: str = None):
        config = configparser.ConfigParser()
        path = os.path.join(os.getcwd(), config_ini_path)
        if not os.path.isfile(path):
            raise Exception('Wrong path for config file: {}'.format(path))
        config.read(path)
        hostname = config.get('Client', 'hostname')
        username = config.get('Client', 'username')
        password = config.get('Client', 'password')
        port = config.getint('Client', 'port')
        self.client_config = ClientConfig(host=hostname, username=username, password=password, port=port)

        ip = config.get('Server', 'ip')
        port = config.getint('Server', 'port')
        rsa_path = config.get('Server', 'rsa_key_path')
        self.server_config = ServerConfig(ip=ip, port=port, key_path=rsa_path)

        out_file_path = config.get('Custom Response', 'out_file_path')
        err_file_path = config.get('Custom Response', 'err_file_path')
        pause = 0 if config.get('Custom Response', 'pause') == '' else config.get('Custom Response', 'pause')

        # TODO move Logs() to ini file
        self.custom_response_config = CustomResponseConfig(out_file_path=out_file_path, log_out_tags=self.log_out_tags,
                                                           log_err_tags=self.log_err_tags,
                                                           err_file_path=err_file_path, pause=pause)
