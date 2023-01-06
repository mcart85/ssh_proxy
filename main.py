import sys

from config_manager import ConfigManager
from custom_response import CustomResponse
from logger import ResponseLogger
from ssh_client import SshClient
from ssh_server import SshServer

args = sys.argv

config_path = 'configuration.ini' if len(args) == 1 else args[1]

config_manager = ConfigManager(config_ini_path=config_path)

custom_response = CustomResponse(config_manager.custom_response_config)

logger = ResponseLogger(config_manager.client_config, log_tags=config_manager.logTags)

ssh_client = SshClient(config_manager.client_config, logger=logger, custom_response=custom_response)

ssh_server = SshServer(ssh_client=ssh_client, config=config_manager.server_config)

ssh_server.run_server()
