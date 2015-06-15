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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Hash')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

import hashlib

class Hash(callbacks.Plugin):
    """An assortment of hashing functions"""
    threaded = True

    def md5(self, irc, msg, args, string):
        """<string>
        
        Creates a md5 hash on <string>
        """
        irc.reply(hashlib.md5(string).hexdigest())
        
    md5 = wrap(md5, ['string'])
    
    def sha1(self, irc, msg, args, string):
        """<string>
        
        Creates a sha1 hash on <string>
        """
        irc.reply(hashlib.sha1(string).hexdigest())
        
    sha1 = wrap(sha1, ['string'])

    def sha224(self, irc, msg, args, string):
        """<string>
        
        Creates a sha-224 hash on <string>
        """
        irc.reply(hashlib.sha224(string).hexdigest())
        
    sha224 = wrap(sha224, ['string'])

    def sha256(self, irc, msg, args, string):
        """<string>
        
        Creates a sha-256 hash on <string>
        """
        irc.reply(hashlib.sha256(string).hexdigest())
        
    sha256 = wrap(sha256, ['string'])
    
    def sha384(self, irc, msg, args, string):
        """<string>
        
        Creates a sha-384 hash on <string>
        """
        irc.reply(hashlib.sha384(string).hexdigest())
        
    sha384 = wrap(sha384, ['string'])
    
    def sha512(self, irc, msg, args, string):
        """<string>
        
        Creates a sha-512 hash on <string>
        """
        irc.reply(hashlib.sha512(string).hexdigest())
        
    sha512 = wrap(sha512, ['string'])

Class = Hash


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
