###
# Copyright (c) 2019, waratte
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

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *

import urllib.request, urllib.parse, urllib.error
from xml.etree import ElementTree

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Alpha')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Alpha(callbacks.Plugin):
    """Provides API access to wolfram alpha"""
    threaded = True

    def alpha(self, irc, msg, args, options, question):
        """[--lines num] <query>

        Ask Mr. Wolfram a question, get an "answer"...maybe? It uses the Wolfram Alpha API.
        <http://products.wolframalpha.com/docs/WolframAlpha-API-Reference.pdf>
        """
        apikey = self.registryValue('apikey')
        if not apikey or apikey == "Not set":
            irc.reply("API key not set. see 'config help supybot.plugins.Wolfram.apikey'.")
            return

	maxoutput = 2
        for (key, value) in options:
            if key == 'lines':
                maxoutput = value

        u = "http://api.wolframalpha.com/v2/query?"
        q = urllib.parse.urlencode({'input': question, 'appid': apikey})
        xml = urllib.request.urlopen(u + q).read()
        tree = ElementTree.fromstring(xml)

        if tree.attrib['success'] == "false":
            for results in tree.findall('.//error'):
                for err in results.findall('.//msg'):
                    irc.reply("Error: " + err.text)
                    return
            irc.reply("huh, I dunno, I'm still a baby AI. Wait till the singularity I guess?")
            return

        found = False
	outputcount = 0
        for pod in tree.findall('.//pod'):
            title = pod.attrib['title']
            for plaintext in pod.findall('.//plaintext'):
                if plaintext.text:
                    found = True
                    """if(title == "Input interpretation" or 
                    title == "Result" or 
                    title == "Input" or 
                    title == "Exact result" or 
                    title == "Decimal approximation"):
                    """
                    if outputcount < maxoutput:
                        output = plaintext.text
                        output = output.replace(' | ', ': ')
                        output = output.replace('\n', ', ')
                        # Skip the input interpretation if only one line out.
                        if maxoutput == 1 and outputcount == 0:
                            maxoutput = 2 # hack :D
                            outputcount += 1
                            continue
                        irc.reply(("%s: %s" % (title, output.encode('utf-8'))))
                        outputcount += 1
        if not found:
            irc.reply("huh, I dunno, I'm still a baby AI. Wait till the singularity I guess?")

    alpha = wrap(alpha, [getopts({'lines':'int'}), 'text'])

Class = Alpha


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
