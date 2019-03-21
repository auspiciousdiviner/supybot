import plugin

import supybot.conf as conf
import supybot.utils as utils
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Wolfram', True)

Wolfram = conf.registerPlugin('Wolfram')
conf.registerGlobalValue(Wolfram, 'apikey', registry.String('Not set', """API key to use WolframAlpha API. A key can be requested at https://developer.wolframalpha.com/.""", private=True))
