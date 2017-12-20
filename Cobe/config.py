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

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Cobe')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Cobe', True)


Cobe = conf.registerPlugin('Cobe')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Cobe, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))

conf.registerGlobalValue(Cobe, 'ignoreRegex', registry.String('^[.@!$%]', _("""Regex to ignore when learning text. Perfect for ignoring commands!""")))
conf.registerGlobalValue(Cobe, 'stripUrls', registry.Boolean(True, _("""Set to true to keep the bot from learning URLs.""")))
conf.registerGlobalValue(Cobe, 'stripNicks', registry.Boolean(False, _("""Set to true to strip all nicks, including the bot's nick, when learning. This replaces it with a special keyword, RECIPIENT.""")))
conf.registerGlobalValue(Cobe, 'recipientString', registry.String('', _("""By default, this is set to nothing. If stripNicks is enabled, it replaces RECIPIENT with this string.""")))
conf.registerChannelValue(Cobe, 'probability', registry.Probability(0, _("""Determines the percent of general messages the bot will answer. Accepts a range of 0 to 1.""")))
conf.registerChannelValue(Cobe, 'probabilityWhenAddressed', registry.Probability(1, _("""Determines the percent of messages addressed to the bot it will answer. Accepts a range of 0 to 1.""")))
conf.registerChannelValue(Cobe, 'waitTimeBetweenSpeaking', registry.NonNegativeInteger(10, _("""Seconds to wait in a channel before speaking again.""")))
conf.registerChannelValue(Cobe, 'ignoreWaitTimeIfAddressed', registry.Boolean(True, _("""Set to true to ignore the wait time, if directly addressed.""")))
conf.registerChannelValue(Cobe, 'responseDelay', registry.Boolean(False, _("""Set to true to delay responding for 2 to 4 seconds in order to seem more human.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
