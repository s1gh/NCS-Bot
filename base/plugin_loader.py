import pkgutil
import sys
from base.helper import Logger

class PluginLoader:
    def __init__(self):
        self.logger = Logger(name=__class__.__name__)
        self.path = 'plugins'
        self.modules = pkgutil.iter_modules(path=['plugins'])
        self.plugins = {}

        for loader, mod_name, ispkg in self.modules:
            if mod_name not in sys.modules:
                try:
                    loaded_module = __import__(self.path + '.' + mod_name, fromlist=[mod_name])
                    #class_name = self.get_class_name(mod_name)
                    loaded_class = getattr(loaded_module, self.get_class_name(mod_name))
                    instance = loaded_class()
                    self.plugins[mod_name] = instance
                except Exception as err:
                    self.logger.error(err)

    def get_plugins(self):
        return self.plugins

    @staticmethod
    def get_class_name(mod_name):
        output = ""
        try:
            words = mod_name.split("_")
        except IndexError:
            words = mod_name
        for word in words:
            output += word.title()
        return output