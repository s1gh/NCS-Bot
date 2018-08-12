import logging
import datetime
from config.config import config

class UserMode:
    @staticmethod
    def give_op(nickname):
        return '+o {}'.format(nickname)

    @staticmethod
    def take_op(nickname):
        return '-o {}'.format(nickname)

    @staticmethod
    def give_voice(nickname):
        return '+v {}'.format(nickname)

    @staticmethod
    def take_voice(nickname):
        return '-v {}'.format(nickname)

class Logger:
    def __init__(self, name=config['nickname'], level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(level)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

class Commands:
    @staticmethod
    def command(plugins, command):
        command = command[1:]
        for plugin in plugins:
            for event in plugin.event_listener.keys():
                if command.split(' ')[0] == event:
                    return plugin
class Uptime:
    def __init__(self, start : datetime):
        self.s = int((datetime.datetime.utcnow() - start).total_seconds())

    def uptime(self):
        m, s = divmod(self.s, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        return '{:0d} days, {:0d} hours, {:0d} minutes and {:0d} seconds'.format(d, h, m, s)

    def __str__(self):
        return self.uptime().strip()
