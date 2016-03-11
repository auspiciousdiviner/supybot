###
# Copyright (c) 2007, Jochen Ritzel
# Based on the original ChanLog code by Jeremiah Fincher, 
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
import supybot.world as world
import supybot.irclib as irclib
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.registry as registry
import supybot.callbacks as callbacks

from Logger import getLogger

class ChanLog(callbacks.Plugin):
    noIgnore = True
    def __init__(self, irc):
        self.__parent = super(ChanLog, self)
        self.__parent.__init__(irc)

        self.lastMsgs = {}
        self.lastStates = {}
        
        world.flushers.append(self.flush)
        
        self.logger = getLogger( self )

    def die(self):
        self.logger.close()
        world.flushers = [x for x in world.flushers
                          if hasattr(x, 'im_class') and
                          x.im_class is not self.__class__]

    def __call__(self, irc, msg):
        try:
            # I don't know why I put this in, but it doesn't work, because it
            # doesn't call doNick or doQuit.
            # if msg.args and irc.isChannel(msg.args[0]):
            self.__parent.__call__(irc, msg)
            if irc in self.lastMsgs:
                if irc not in self.lastStates:
                    self.lastStates[irc] = irc.state.copy()
                self.lastStates[irc].addMsg(irc, self.lastMsgs[irc])
        finally:
            # We must make sure this always gets updated.
            self.lastMsgs[irc] = msg

    def reset(self):
        self.logger.reset()

    def flush(self):
        self.logger.flush()

    def doPrivmsg(self, irc, msg):
        (recipients, text) = msg.args
        for channel in recipients.split(','):
            if irc.isChannel(channel):
                nick = msg.nick or irc.nick
                if ircmsgs.isAction(msg):
                    self.logger.getLog(irc, channel).doAction(nick, ircmsgs.unAction(msg))
                else:
                    noLogPrefix = self.registryValue('noLogPrefix', channel)
                    if noLogPrefix and text.startswith(noLogPrefix):
                        self.logger.getLog(irc, channel).doMessage(nick, text, True)
                    else:
                        self.logger.getLog(irc, channel).doMessage(nick, text, False)

    def doNotice(self, irc, msg):
        (recipients, text) = msg.args
        for channel in recipients.split(','):
            if irc.isChannel(channel):
                self.logger.getLog(irc, channel).doNotice(msg.nick, text)

    def doNick(self, irc, msg):
        oldNick = msg.nick
        newNick = msg.args[0]
        for (channel, c) in irc.state.channels.iteritems():
            if newNick in c.users:
                self.logger.getLog(irc, channel).doNick(oldNick, newNick)
                
    def doJoin(self, irc, msg):
        for channel in msg.args[0].split(','):
            self.logger.getLog(irc, channel).doJoin(msg.nick or msg.prefix, channel)

    def doKick(self, irc, msg):
        if len(msg.args) == 3:
            (channel, target, kickmsg) = msg.args
        else:
            (channel, target) = msg.args
            kickmsg = ''
        self.logger.getLog(irc, channel).doKick(target, msg.nick, kickmsg)

    def doPart(self, irc, msg):
        for channel in msg.args[0].split(','):
            self.logger.getLog(irc, channel).doPart(msg.nick, channel)

    def doMode(self, irc, msg):
        channel = msg.args[0]
        if irc.isChannel(channel) and msg.args[1:]:
            self.logger.getLog(irc, channel).doMode(msg.nick or msg.prefix, msg.args[1:])

    def doTopic(self, irc, msg):
        if len(msg.args) == 1:
            return # It's an empty TOPIC just to get the current topic.
        channel = msg.args[0]
        self.logger.getLog(irc, channel).doTopic(msg.nick, msg.args[1])

    def doQuit(self, irc, msg):
        if not isinstance(irc, irclib.Irc):
            irc = irc.getRealIrc()
        for (channel, chan) in self.lastStates[irc].channels.iteritems():
            if msg.nick in chan.users:
                self.logger.getLog(irc, channel).doQuit(msg.nick)
    
    def outFilter(self, irc, msg):
        # Gotta catch my own messages *somehow* :)
        # Let's try this little trick...
        if msg.command in ('PRIVMSG', 'NOTICE'):
            # Other messages should be sent back to us.
            m = ircmsgs.IrcMsg(msg=msg, prefix=irc.prefix)
            self(irc, m)
        return msg


Class = ChanLog
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
