"""Main class for PromBZEx"""
from . import config
from . import server


class PromBZEx:
    """Main class"""
    config = None

    def __init__(self, configpath):
        self.config = config.PromBZExConfig(configpath)

    def config_get(self, key, server_name=None, allow_default=True):
        """Return a config item"""
        return self.config.get(key, server_name, allow_default)

    def servers(self):
        """Return the names of our servers"""
        return self.config.servers()

    def server(self, name):
        """Return an instance of BZServer"""
        return server.BZServer(name, self.config)
