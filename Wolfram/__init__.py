"""
Does stuff with Wolfram Alpha webservice.
"""

import supybot
import supybot.world as world

__version__ = "0.1"
__author__ = "Ed Summers"
__contributors__ = {}
__url__ = '' 

import config
import plugin
reload(plugin) # In case we're being reloaded.
reload(config)

if world.testing:
    import test

Class = plugin.Class
configure = config.configure
