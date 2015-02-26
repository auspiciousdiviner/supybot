###
# Copyright (c) 2015, waratte
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import urllib
from urllib import request 
from bs4 import BeautifulSoup

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('PoIEpisodeDirectory')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class PoIEpisodeDirectory(callbacks.Plugin):
    """Add the help for "@plugin help PoIEpisodeDirectory" here
    This should describe *how* to use this plugin."""
    pass

    def __init__(self, irc):
        self.__parent = super(Random, self)
        self.__parent.__init__(irc)
        self.episodes_url_path = "http://www.tv.com/shows/person-of-interest-2011/episodes/"
        self.episodes_season_url_path = "http://www.tv.com/shows/person-of-interest-2011/" 
        
    def poi(self, irc, msg, args, season, episode):
        """<season> <episode>
        
        Gets the synopsis of Person of Interest episode <episode> of season <season>.
        """
        
        req = urllib.request.Request(
            "%sseason-%d".format(self.episodes_season_url_path, season),
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
            }
        )

        soup = BeautifulSoup(urllib.request.urlopen(req).read())
         
        element = soup.find("ul", class_="filters")
         
        for element1 in element.find_all("strong"):
            if element1.get_text() != 'All':
            irc.reply(element1.get_text()) 
        
    poi = wrap(poi, ['text', 'int', 'int'])


Class = PoIEpisodeDirectory


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
