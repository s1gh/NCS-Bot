class Help:
    """Help Plugin: Get help on plugins and related functions"""
    def __init__(self):
        self.event_listener = {
            'help': 'get_help'
        }

    def get_help(self, con, event):
        from main import bot
        plugins = bot.loaded_plugins

        if len(event.message) == 0:
            con.notice(event.target, 'Print general help menu here...')

        try:
            class_doc_string = plugins[event.message].__doc__
        except KeyError:
            con.notice(event.target, 'Error :: This plugin does not exist!')
        else:
            try:
                con.notice(event.target, ''.join(class_doc_string.splitlines()))
            except AttributeError:
                con.notice(event.target, 'Error :: This plugin does not have a docstring!')