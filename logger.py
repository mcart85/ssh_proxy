import os
from datetime import datetime

from config_manager import ClientConfig, LogTags


class ResponseLogger:
    def __init__(self, client_config: ClientConfig, log_out_tags: LogTags, log_err_tags: LogTags):
        self.hostname = client_config.hostname.replace(".", "_")
        self.timestamp = None
        self.out_file = None
        self.err_file = None
        self.log_out_tags = log_out_tags
        self.log_err_tags = log_err_tags

    def get_time_stamp(self) -> str:
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime('%d_%m_%H-%M')
            os.mkdir(os.path.join(os.getcwd(), self.timestamp))
        return self.timestamp

    def get_out_path(self) -> str:
        if self.out_file is None:
            self.out_file = r'{}\{}\out_{}.txt'.format(os.getcwd(), self.get_time_stamp(), self.hostname)
        return self.out_file

    def get_err_path(self) -> str:
        if self.err_file is None:
            self.err_file = r'{}\{}\err_{}.txt'.format(os.getcwd(), self.get_time_stamp(), self.hostname)
        return self.err_file

    def log_out(self, is_custom: bool, command: str, out):
        self.write_log(command=command, is_custom=is_custom, body=out, path=self.get_out_path(), tags=self.log_out_tags)

    def log_error(self, command, is_custom, err):
        self.write_log(command=command, is_custom=is_custom, body=err, path=self.get_err_path(), tags=self.log_err_tags)

    def write_log(self, command: str, body: str, is_custom: bool, path: str, tags: LogTags):
        if len(body) > 0:
            with open(file=path, mode="a", encoding="utf-8") as file:
                message = "{}{}\n{}{}{}\n".format(tags.command_tag, command, tags.start_tag,
                                                  body, tags.end_tag)
                if is_custom:
                    message = "CUSTOM RESPONSE\n" + message
                file.write(message)
