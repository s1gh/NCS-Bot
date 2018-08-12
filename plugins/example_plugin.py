import datetime
from base.helper import Uptime, Logger

class ExamplePlugin:
    """Example Plugin: Example plugin for easier development of new functionality."""
    def __init__(self):
        self.logger = Logger(__class__.__name__)
        self.uptime = datetime.datetime.now()
        self.event_listener = {
            'ping': 'ping',
            'uptime': 'uptime',
            'topic': 'topic',
            'echo': 'echo'
        }

    def ping(self, con, event):
        self.logger.info('Logging example from ExamplePlugin!!!')
        con.privmsg(event.target, '!pong')

    def uptime(self, con, event):
        con.privmsg(event.target, 'Current Uptime: {}'.format(Uptime(self.uptime)))

    def topic(self, con, event):
        con.topic(event.target, event.message)

    def echo(self, con, event):
        con.privmsg(event.target, event.message)