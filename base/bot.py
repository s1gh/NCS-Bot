import logging
import irc.bot
import sys
import importlib
from config.config import config
from base.helper import Commands
from base.plugin_loader import PluginLoader

if config['tls']:
    import ssl
    from irc.connection import Factory

logger = logging.getLogger('NCSBot')

class NCSBot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        ssl_factory = Factory(wrapper=ssl.wrap_socket) if config['tls'] else None
        self.loaded_plugins = PluginLoader().get_plugins()

        super().__init__(server_list=[(config['server'], config['port']), ], nickname=config['nickname'],
                         realname=config['realname'])

    def get_loaded_plugins(self):
        return self.loaded_plugins

    def load_plugin(self, plugin):
        try:
            module = importlib.import_module('plugins.{}'.format(plugin))
            self.loaded_plugins[plugin] = getattr(module, PluginLoader.get_class_name(plugin))()
        except ImportError:
            return False
        return True

    def unload_plugin(self, plugin):
        try:
            del self.loaded_plugins[plugin]
            del sys.modules['plugins.{}'.format(plugin)]
        except KeyError:
            return False
        return True

    def reload_plugin(self, plugin):
        try:
            module = importlib.reload(sys.modules['plugins.{}'.format(plugin)])
            self.loaded_plugins[plugin] = getattr(module, PluginLoader.get_class_name(plugin))()
        except KeyError as err:
            return False
        return True

    def on_nicknameinuse(self, connection, event):
        logger.info('Nickname already in use. Trying alternative nickname ...')

        if connection.nick == config['nickname_alt']:
            logger.info('Alternative nickname already in use. Appending _ to nickname ...')
            connection.nick(connection.get_nickname() + '_')

        connection.nick(config['nickname_alt'])

    def on_welcome(self, connection, event):
        logger.info('Connected to IRC Server!')

        try:
            connection.oper(config['oper_username'], config['oper_password'])
            for channel in config['channels']:
                connection.join(channel)
                connection.mode(channel, '+o {}'.format(connection.get_nickname()))  # Set OP on self in every channel
        except Exception as err:
            logger.error(err)
            pass

        logger.info('Loaded {} plugin(s): {}'.format(len(self.loaded_plugins), ','.join(self.loaded_plugins.keys())))

    def on_disconnect(self, connection, event):
        logger.warning('Lost connection to IRC server. Trying to reconnect ...')

    def on_mode(self, connection, event):
        # You can't touch me!
        connection.mode(event.target, '+o {}'.format(connection.get_nickname()))

    def on_privmsg(self, connection, event):
        cmd = event.arguments[0].split(' ')[0][1:]
        message = event.arguments[0][len(cmd) + 1:].strip()
        source = event.source.split('!')[0]

        if cmd == 'unload' and len(message) > 0:
            if self.unload_plugin(message):
                connection.privmsg(source, 'Info :: Plugin unloaded successfully.')
            else:
                connection.privmsg(source, 'Error :: Could not unload plugin.')

        elif cmd == 'reload' and len(message) > 0:
            if self.reload_plugin(message):
                connection.privmsg(source, 'Info :: Plugin reloaded successfully.')
            else:
                connection.privmsg(source, 'Error :: Could not reload plugin.')

        elif cmd == 'load' and len(message) > 0:
            if self.load_plugin(message):
                connection.privmsg(source, 'Info :: Plugin loaded successfully.')
            else:
                connection.privmsg(source, 'Error :: Could not load plugin.')

    def on_pubmsg(self, connection, event):
        plugin = Commands.command(self.loaded_plugins.values(), event.arguments[0].split(' ')[0])
        cmd = event.arguments[0].split(' ')[0][1:]
        event.message = event.arguments[0][len(cmd) + 1:].strip()

        if event.arguments[0].startswith(config['command_prefix']) and plugin is not None:
            try:
                getattr(plugin, plugin.event_listener[cmd])(connection, event)
            except AttributeError as err:
                logger.error('Event listener not registered for this command ({})'.format(cmd))

    def on_privnotice(self, connection, event):
        logger.info(event.arguments)
