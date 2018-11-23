"""Main class for PromBZEx"""
import os

from . import config
from . import server


class PromBZEx:
    """Main class"""
    config = None

    def __init__(self, config_file):
        self.config = config.PromBZExConfig(config_file)

    def config_get(self, key, server_name=None, allow_default=True):
        """Return a config item"""
        return self.config.get(key, server_name, allow_default)

    def servers(self):
        """Return the names of our servers"""
        return self.config.servers()

    def server(self, name):
        """Return an instance of BZServer"""
        return server.BZServer(name, self.config)

    def write(self, output, server_name=None):
        """Write output to a Prometheus file, possibly per-server"""
        filename = "bugzilla.prom"
        if server_name:
            filename = self.config_get('output_file', server_name)

        outfile = os.path.join(self.config_get('output_dir'), filename)
        with open(outfile, 'w') as filep:
            filep.write(output)
