#!/usr/bin/env python3
"""Configuration for Prombzex"""

import configparser


class PrombzexConfig:
    """This class abstracts the INI config file. Its format is:
    [DEFAULT]
    Foo = bar

    [some.bugzilla.server.com]
    Baz = Bing"""

    data = None

    def __init__(self, config_path):
        """Initialise the class and load the config"""
        self.data = configparser.ConfigParser()
        self.data.read(config_path)

    def servers(self):
        """Return a list of configured BZ servers"""
        return self.data.sections()

    def get(self, key, server=None):
        """Return a config value for a given key, optionally for a
        specific server. If no server is specified, the default
        value is returned. If a server is specified, its value is
        returned, unless it defines no value, in which case the
        default is returned.
        If neither the specified server, nor the defaults, have a
        value for the key, None will be returned"""

        value = None

        if key in self.data['DEFAULT']:
            value = self.data['DEFAULT'][key]

        if server and key in self.data[server]:
            value = self.data[server][key]

        return value
