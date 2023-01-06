import os
import time
from typing import Dict

from config_manager import CustomResponseConfig


class CustomResponse():
    def __init__(self, custom_resp_config: CustomResponseConfig):
        self.tags = custom_resp_config.log_tags
        self.out_file_path = custom_resp_config.out_path
        self.err_file_path = custom_resp_config.err_path
        self.out_response = None
        self.err_response = None
        self.create_response_dict()
        self.pause = custom_resp_config

    def create_response_dict(self):
        self.out_response = self.read_custom_resp_file(path=self.out_file_path,
                                                       com_tag=self.tags.command_tag,
                                                       start_tag=self.tags.out_start_tag,
                                                       end_tag=self.tags.out_end_tag)

        self.err_response = self.read_custom_resp_file(path=self.err_file_path,
                                                       com_tag=self.tags.command_tag,
                                                       start_tag=self.tags.error_start_tag,
                                                       end_tag=self.tags.error_end_tag)

    def read_custom_resp_file(self, path, com_tag, start_tag, end_tag) -> Dict[str, bytes]:
        custom_responses = {'': b''}
        if os.path.isfile(path):
            with open(file=path, mode='r',encoding='utf-8') as file:
                while True:
                    line = file.readline()
                    if line == '':
                        break
                    if line.startswith(com_tag):
                        command = line[len(com_tag):].replace('\n', '')
                    if line.startswith(start_tag):
                        line = file.readline()
                        output = []
                        while not line.startswith(end_tag):
                            output.append(line)
                            line = file.readline()
                        custom_responses.update({command: bytes("".join(output), 'utf-8')})
        return custom_responses

    def has_custom_response(self, command: str) -> bool:
        # TODO resolve it on config level
        if "cat /var/log/messages" in command:
            return True
        return command in self.out_response or command in self.err_response

    def get_custom_response(self, command: str):
        time.sleep(self.pause)
        # TODO resolve it on config level
        if "cat /var/log/messages" in command:
            return bytes(
                'Dec 19 00:06:57 122CE-4 zabbix_agentd: zabbix_agentd [82633]: ERROR: StartAgents is not 0, parameter "Server" must be defined\n',
                'utf-8'), b''
        out = b'' if command not in self.out_response else self.out_response[command]
        err = b'' if command not in self.err_response else self.err_response[command]
        return out, err
