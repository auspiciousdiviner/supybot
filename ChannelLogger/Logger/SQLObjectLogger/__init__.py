from .FakeLog import FakeLog
import datetime
from model import *

class SQLObjectLogFactory(object):
    def __init__(self, URI):
        # i fucking hate encodings. This string is encoded here, next by SQLObject, then the DB adapter takes it's shot again
        # i tried to make this work somehow, but mysql is giving me a hard time
        import sqlobject
        from SQLObject_model import Log, Channel
        from SQLObjectLog import SQLObjectLog
        
        # set up a connection
        connection = sqlobject.connectionForURI( URI, sqlobject_encoding='utf-8')
        sqlobject.sqlhub.processConnection = connection
        
        #make sure we have all  used tables
        Channel.createTable(ifNotExists=True)
        Log.createTable(ifNotExists=True)
        
        #create a factory function
        def createLog( irc, channel ):
            return SQLObjectLog( irc, channel)
        self.createLog = createLog


class SQLObjectLog(FakeLog):
    """Logs one channel into the database"""
    def __init__(self, irc, channel):
        # get the correct Channel Object
        network = str(irc.network)
        channel = channel.lstrip('#')
        c = Channel.selectBy(network=network, name=channel)
        if c.count() == 0:
            c = Channel(network = network, name=channel)
        else:
            c = c[0]
        def doLog(m, nick, *args):
            #assume stuff is latin-1, im sick and tired of this encoding faggotry.
            # mysqlobject is a faggot too, reencoding this again
            # i hope sqlobject 0.9.1 fixed this, i had to hack mysqlconnection.py #112  >_<
            text = ' '.join(args).decode('cp1252')
            Log( channel=c, created_on=datetime.datetime.now(), type=m, nick=nick, text=text)
        self.doLog = doLog

    def doNotice(self, nick, text):
        self.doLog('notice', nick, text)
    def doAction(self, nick, action):
        self.doLog('action', nick, action)
    def doMessage(self, nick, text, private):
        if private:
            self.doLog('private', nick, text)
        else:
            self.doLog('message', nick, text)
    def doNick(self, oldNick, newNick):
        self.doLog('nickchange', oldNick, newNick)
    def doJoin(self, nick, channel):
        self.doLog('join', nick, channel)
    def doKick(self, target, nick, kickmsg=''):
        self.doLog('kick', nick, target, kickmsg)
    def doPart(self, nick, channel):
        self.doLog('part', nick, channel)
    def doMode(self, nick, modes):
        self.doLog('mode', nick, ' '.join(modes) )
    def doTopic(self, nick, topic):
        self.doLog('topic', nick, topic)
    def doQuit(self, nick):
        self.doLog('quit', nick)
