import os
from datetime import datetime

from config_manager import ClientConfig, LogTags


class ResponseLogger():
    def __init__(self, client_config: ClientConfig, log_tags: LogTags):
        self.hostname = client_config.hostname.replace(".", "_")
        self.timestamp = None
        self.out_file = None
        self.err_file = None
        self.tags = log_tags

    def get_time_stamp(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime('%d_%m_%H-%M')
            os.mkdir(os.path.join(os.getcwd(), self.timestamp))
        return self.timestamp

    def get_out_path(self):
        if self.out_file is None:
            self.out_file = r'{}\{}\out_{}.txt'.format(os.getcwd(), self.get_time_stamp(), self.hostname)
        return self.out_file

    def get_err_path(self):
        if self.err_file is None:
            self.err_file = r'{}\{}\err_{}.txt'.format(os.getcwd(), self.get_time_stamp(), self.hostname)
        return self.err_file

    def log_out(self, is_custom: bool, command: str, out):
        if len(out) > 0:
            with open(file=self.get_out_path(), mode="a", encoding="utf-8") as out_file:
                message = "{}{}\n{}{}{}\n".format(self.tags.command_tag, command, self.tags.out_start_tag, out,
                                                  self.tags.out_end_tag)
                if is_custom:
                    message = "CUSTOM RESPONSE\n" + message
                out_file.write(message)
                print(message)

    def log_error(self, is_custom: bool, command, err):
        if len(err) > 0:
            with open(file=self.get_err_path(), mode="a", encoding="utf-8") as err_file:
                message = "{}{}\n{}{}{}\n".format(self.tags.command_tag, command, self.tags.error_start_tag,
                                                  err,
                                                  self.tags.error_end_tag)
                if is_custom:
                    message = "CUSTOM RESPONSE\n" + message
                err_file.write(message)
                print(message)
