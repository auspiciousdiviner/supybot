import supybot.conf as conf
import supybot.registry as registry
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('Random')

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Random', True)


Random = conf.registerPlugin('Random')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Random, 'someConfigVariableName',
#     registry.Boolean(False, _("""Help for someConfigVariableName.""")))

conf.registerGlobalValue(Random, 'maxCoins',
    registry.PositiveInteger(50000, _("""The maximum amount of coins that can be flipped""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
