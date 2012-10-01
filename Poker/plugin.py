import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import glob
import os
import re

_ = PluginInternationalization('Poker')

"""
try:
    with open(conf.supybot.directories.data.dirize('holdem_user.db')) as f: pass
except IOError:
    with open(conf.supybot.directories.data.dirize('holdem_user.db'), 'w') as file:
        file.writelines('')
try:
    with open(conf.supybot.directories.data.dirize('holdem_money.db')) as f: pass
except IOError:
    with open(conf.supybot.directories.data.dirize('holdem_money.db'), 'w') as file:
        file.writelines('')
"""

dataDir =  conf.supybot.directories.data
pokerDirectory = dataDir.dirize('Poker/')


@internationalizeDocstring
class Poker(callbacks.Plugin):
    """Contains lots of commands to aid you in making your own Texas Hold'em games through IRC; use the 'create' command to start, 
       everything afterwards is self-explantory.

    """
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Poker, self)
        self.__parent.__init__(irc)
        
        if not os.path.exists( pokerDirectory ):
            os.makedirs( pokerDirectory )

    def create(self, irc, msg, args, var):
        """<game_name>

        Sets up a table to play Texas Hold'em on partner.
        """
        
        pokerGameFile = open( pokerDirectory + 'poker_game_' + var + '.db', 'w')
        #pokerGameFile.write('')

        irc.replySuccess(format('Table \"%s\" was created partner.', var))
    create = wrap(create, ['text'])

    def destroy(self, irc, msg, args, var):
        """<game_name>

        We throw the table out when you're done playing Texas Hold'em, partner.
        """
        if not os.path.exists( pokerDirectory + 'poker_game_' + var + '.db'):
            irc.replyError(format('Table \"%s\" doesn\'t exist, are you hallucinating partner?', var))
        else:
            os.remove( pokerDirectory + 'Table_' + var + '.db')
            irc.replySuccess(format('Table \"%s\" was thrown out partner.', var))

    destroy = wrap(destroy, ['text'])

    def tables(self, irc, msg, args):
        """This command takes no aruguments

        Lists all the available tables, partner.
        """

        listOfTables =  os.listdir( pokerDirectory )

        irc.reply( '%s' % ''.join( map( str, listOfTables )))
    tables = wrap(tables)

Class = Poker


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
