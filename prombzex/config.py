#!/usr/bin/env python3
"""Configuration for Prombzex"""

import json


class PromBZExConfig:
    """This class abstracts the json config file. Its format is:
    TODO: document the format"""

    data = None

    def __init__(self, config_file_object):
        """Initialise the class and load the config"""
        self.data = json.load(config_file_object)

    def servers(self):
        """Return a list of configured BZ servers"""
        return list(filter(lambda x: x != "default", self.data.keys()))

    def server(self, name):
        """Return the data for a server"""
        return self.data[name]

    def get(self, key, server=None, allow_default=True):
        """Return a config value for a given key, optionally for a
        specific server. If no server is specified, the default
        value is returned. If a server is specified, its value is
        returned, unless it defines no value, in which case the
        default is returned.
        If neither the specified server, nor the defaults, have a
        value for the key, None will be returned"""

        value = None

        if allow_default and 'default' in self.data and \
                key in self.data['default']:
            value = self.data['default'][key]

        if server and key in self.data[server]:
            value = self.data[server][key]

        return value
