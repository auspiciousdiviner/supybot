from sqlalchemy import create_engine
from sqlalchemy.sql import select
from supybot import ircutils
import datetime

import model
from ..BaseLogger import BaseLog, BaseLogFactory

class SQLAlchemyLogFactory(BaseLogFactory):
    def __init__(self, config):
        super(SQLAlchemyLogFactory, self).__init__( config )
        URI = config.registryValue('SQLAlchemy.URI')
        engine = create_engine( URI )
        model.metadata.create_all( engine )
        self.connection = engine.connect()
            
    def createLog(self, irc, channel):
        network = str(irc.network)
        name = channel.lstrip('#')
        # look if we have a row for the channel already 
        result = self.connection.execute(       select([model.channels.c.id], 
                                                            (model.channels.c.network==network) & (model.channels.c.name==name)) 
                                                    ).fetchone()
        if result is None:
            # create the channel
            result = self.connection.execute( model.channels.insert( values=dict(network = network, name=name)) )
            channel_id = result.last_inserted_ids()[0]
        else:
            channel_id = result.id
            
        insert = model.logs.insert( values=dict(channel_id = channel_id))
        stripFormatting = self.config.registryValue('stripFormatting', channel)
        return SQLAlchemyLog( self.connection, insert, stripFormatting )

class SQLAlchemyLog(BaseLog):
    """Logs one channel into the database"""
    def __init__(self, conn,query, stripFormatting=True):
        self.query = query
        self.conn = conn
        self.stripFormatting = stripFormatting
        
    def doLog(self, m, nick, *args):
        text = unicode(' '.join(args), 'cp1252', 'replace')
        if self.stripFormatting:
            text = ircutils.stripFormatting(text) 
        self.conn.execute(self.query,  created_on=datetime.datetime.now(), type=m, nick=nick, text=text)
    def doNotice(self, nick, text):
        self.doLog(model.NOTICE , nick, text)
    def doAction(self, nick, action):
        self.doLog(model.ACTION, nick, action)
    def doMessage(self, nick, text, private):
        if private:
            self.doLog(model.PRIVATE, nick, text)
        else:
            self.doLog(model.MESSAGE, nick, text)
    def doNick(self, oldNick, newNick):
        self.doLog(model.NICKCHANGE, oldNick, newNick)
    def doJoin(self, nick, channel):
        self.doLog(model.JOIN, nick, channel)
    def doKick(self, target, nick, kickmsg=''):
        self.doLog(model.KICK, nick, target, kickmsg)
    def doPart(self, nick, channel):
        self.doLog(model.PART, nick, channel)
    def doMode(self, nick, modes):
        self.doLog(model.MODE, nick, ' '.join(modes) )
    def doTopic(self, nick, topic):
        self.doLog(model.TOPIC, nick, topic)
    def doQuit(self, nick):
        self.doLog(model.QUIT, nick)
