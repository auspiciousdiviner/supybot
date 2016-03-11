# This code is mostly the original ChanLog code by Jeremiah Fincher, 
# extracted and restructured into its own class 
import os
import time

from supybot import conf
from supybot import ircutils

from ..BaseLogger import BaseLog, BaseLogFactory

class FileLogFactory(BaseLogFactory):
    def createLog(self, irc, channel ):
        return FileLog( irc, channel, self.config )

class FileLog(BaseLog):
    """Logs one channel to one file"""
    def __init__(self, irc, channel, config ):
        self.config = config       
        self.channel = channel.lower()
        self.irc = irc
        self.CurrentLogName = self.getCurrentLogName()
        self.LogFile = open( self.CurrentLogName,'a')
    
    def close(self):
        self.LogFile.close()
    def flush(self):
        self.LogFile.flush()
        
    def getCurrentLogName(self):
        name = self.getLogName()
        logDir = self.getLogDir()
        return os.path.join(logDir, name)
      
    def logNameTimestamp(self):
        return time.strftime(self.config.registryValue('File.filenameTimestamp', self.channel))

    def getLogName(self):
        if self.config.registryValue('File.rotateLogs', self.channel):
            return '%s.%s.log' % (self.channel, self.logNameTimestamp())
        else:
            return '%s.log' % self.channel

    def getLogDir(self):
        logDir = conf.supybot.directories.log.dirize(self.config.name())
        if self.config.registryValue('File.directories'):
            if self.config.registryValue('File.directories.network'):
                logDir = os.path.join(logDir,  self.irc.network)
            if self.config.registryValue('File.directories.channel'):
                logDir = os.path.join(logDir, self.channel)
            if self.config.registryValue('File.directories.timestamp'):
                format = self.config.registryValue('File.directories.timestamp.format')
                timeDir =time.strftime(format)
                logDir = os.path.join(logDir, timeDir)
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        return logDir
  
    def timestamp(self):
        format = conf.supybot.log.timestampFormat()
        if format:
            self.LogFile.write(time.strftime(format))
            self.LogFile.write('  ')

    def doLog(self, s, *args):
        ## the actual logging that calls this function is inherited from the BaseLog
        text = format(s, *args)
        if self.getCurrentLogName() != self.CurrentLogName:
            self.LogFile.close()
            self.LogFile = open(self.getCurrentLogName(),'a')
        if self.config.registryValue('File.timestamp', self.channel):
            self.timestamp()
        if self.config.registryValue('stripFormatting', self.channel):
            text = ircutils.stripFormatting(text) 
        self.LogFile.write(text)
        if self.config.registryValue('File.flushImmediately'):
            self.flush()