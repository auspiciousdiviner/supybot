class BaseLogFactory( object ):
    def __init__(self, config):
        self.config = config
        self.logs = {}

    def getLog(self, network, channel ):
        key = (network, channel)
        if key in self.logs:
            return self.logs[ key ]
        else:
            log = self.createLog( network, channel )
            self.logs[ key ] = log
            return log

    def createLog(self, network, channel):
        return BaseLog()

    def reset(self):
        pass
        
    def close(self):
        for log in self.logs.values():
            log.close()
    def flush(self):
        for log in self.logs.values():
            log.flush()
        
class BaseLog(object):
    """Dummy class to jump in if something is wrong with the real log"""
    def doLog(self, s, *args):
        print "%s wants to log: '%s'" % ( self.__class__.__name__ , format(s, *args) )
    def doNotice(self, nick, text):
        self.doLog('-%s- %s\n', nick, text)
    def doAction(self, nick, action):
        self.doLog('* %s %s\n', nick, action)
    def doMessage(self, nick, text):
        self.doLog('<%s> %s\n', nick, text)
    def doNick(self, oldNick, newNick):
        self.doLog('*** %s is now known as %s\n', oldNick, newNick)
    def doJoin(self, nick, channel):
        self.doLog('*** %s has joined %s\n', nick, channel)
    def doKick(self, target, nick, kickmsg=None):
        if kickmsg:
            self.doLog('*** %s was kicked by %s (%s)\n',target, nick, kickmsg)
        else:
            self.doLog('*** %s was kicked by %s\n', target, nick)
    def doPart(self, nick, channel):
        self.doLog('*** %s has left %s\n', nick, channel)
    def doMode(self, nick, modes):
        self.doLog('*** %s sets mode: %s\n', nick, ' '.join(modes) )
    def doTopic(self, nick, topic):
        self.doLog('*** %s changes topic to "%s"\n', nick, topic)
    def doQuit(self, nick):
        self.doLog('*** %s has quit IRC\n', nick)

    def close(self):
        pass
    def flush(self):
        pass
