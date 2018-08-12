from base.helper import UserMode, Logger
from base.plugin_loader import PluginLoader

class Admin:
    def __init__(self,):
        self.logger = Logger(__class__.__name__)
        self.event_listener = {
            'giveop': 'give_op',
            'takeop': 'take_op',
            'givevoice': 'give_voice',
            'takevoice': 'take_voice'
        }

    def give_op(self, con, event):
        con.mode(event.target, UserMode.give_op(event.message))

    def take_op(self, con, event):
        con.mode(event.target, UserMode.take_op(event.message))

    def give_voice(self, con, event):
        con.mode(event.target, UserMode.give_voice(event.message))

    def take_voice(self, con, event):
        con.mode(event.target, UserMode.take_voice(event.message))