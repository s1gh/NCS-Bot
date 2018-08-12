from base.helper import Logger, UserMode

class Noc:
    """NOC Plugin: Plugin for managing NOC responsibilities etc."""
    def __init__(self):
        self.logger = Logger(__class__.__name__)
        self.event_listener = {
            'vakt': 'set_noc_responsibility'
        }

    def set_noc_responsibility(self, con, event):  # Keep an internal record of responsibilities
        if event.message:
            con.mode(event.target, UserMode.give_op(event.message))
        else:
            con.mode(event.target, UserMode.give_op(event.source.split('!')[0]))