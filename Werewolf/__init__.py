###
# Copyright (c) 2010, Julian Aloofi
# All rights reserved.
#
#    This file is part of supybot-werewolf.
#
#    supybot-werewolf is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    supybot-werewolf is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with supybot-werewolf.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
###
"""
Leads and moderates a werewolf game (aka "mafia")
If you're planning to run the bot on Freenode or OFTC,
read the accompanying README.txt!
"""

import supybot
import supybot.world as world

# Use this for the version of this plugin.  You may wish to put a CVS keyword
# in here if you're keeping the plugin in CVS or some similar system.
__version__ = "0.6"

# XXX Replace this with an appropriate author or supybot.Author instance.
__author__ = supybot.Author('Julian Aloofi', 'nailuj24',
                                'julian.fedora@gmail.com')

# This is a dictionary mapping supybot.Author instances to lists of
# contributions.
__contributors__ = {}

# This is a url where the most recent plugin package can be downloaded.
__url__ = 'https://launchpad.net/supybot-werewolf' 

import config
import plugin
reload(plugin) # In case we're being reloaded.
# Add more reloads here if you add third-party modules and want them to be
# reloaded when this plugin is reloaded.  Don't forget to import them as well!

if world.testing:
    import test

Class = plugin.Class
configure = config.configure


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
