import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import glob
import os

_ = PluginInternationalization('Holdem')

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
holdemDirectory = dataDir.dirize('Holdem/')


@internationalizeDocstring
class Holdem(callbacks.Plugin):
    """Contains lots of commands to aid you in making your own Texas Hold'em games through IRC; use the 'create' command to start, 
       everything afterwards is self-explantory.

    """
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Holdem, self)
        self.__parent.__init__(irc)
        
        if not os.path.exists( holdemDirectory ):
            os.makedirs( holdemDirectory )

    def create(self, irc, msg, args, var):
        """<game_name>

        Sets up a table to play Texas Hold'em on partner.
        """
        
        irc.reply( holdemDirectory + 'holdem_game_' + var + '.db' )
        holdemGameFile = open( holdemDirectory + 'holdem_game_' + var + '.db', 'w')
        #holdemGameFile.write('')

        irc.replySuccess(format('Table \"%s\" was created partner.', var))
    create = wrap(create, ['text'])

    def tables(self, irc, msg, args):
        """This command takes no aruguments

        Lists all the available tables, partner.
        """

<<<<<<< HEAD
        listOfTables = glob.glob(conf.supybot.directories.data.dirize('/Holdem/holdem_game_*.db'))

        irc.reply(listOfTables)
=======
        listOfTables = os.path.basename( glob.glob( holdemDirectory + 'holdem_game_*.db'))

        irc.reply( map( str, listOfTables ))
>>>>>>> Lots of stuff!
    tables = wrap(tables)

Class = Holdem


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
