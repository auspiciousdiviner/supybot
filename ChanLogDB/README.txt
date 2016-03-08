This is just a slightly modified version of Jochen Ritzel's Channel Logger plugin here: https://bitbucket.org/THC4k/supybot-channellogger

The modifications made were just to make it useful for my channel stats webapp.

It now logs messages that are meant not to be logged, but sets a private flag for that message, leaving the admin to do whatever he wants with the message.

====

Old readme:

This plugin is a full replacement for the Channellogger plugin.
Besides having the ability to log to a file, it can log to most databases through SQLAlchemy. 
Obviously you will need SQLAlchemy ( http://www.sqlalchemy.org ) and maybe a database adapter ( ie. http://sourceforge.net/projects/mysql-python/ ) to make this work.

To use it, replace the old channellogger with this plugin, then 

set supybot.plugins.ChannelLogger.File False
set supybot.plugins.ChannelLogger.SQLAlchemy True
set supybot.plugins.ChannelLogger.SQLAlchemy.URI <Your DB URI>

where <Your DB URI> looks like this:
 scheme://[user[:password]@]host[:port]/database[?parameters]

Examples:
mysql://user:password@host/database
mysql://host/database?debug=1
postgres://user@host/database?debug=&cache=
postgres:///full/path/to/socket/database
postgres://host:5432/database
sqlite:///full/path/to/database
sqlite:/C|/full/path/to/database
sqlite:/:memory:
