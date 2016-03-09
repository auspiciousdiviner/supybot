Besides having the ability to log to a file, it can log to most databases through SQLAlchemy. 
Obviously you will need SQLAlchemy ( http://www.sqlalchemy.org ) and maybe a database adapter ( ie. http://sourceforge.net/projects/mysql-python/ ) to make this work.

To use it, replace the old channellogger with this plugin, then 

set supybot.plugins.ChanLog.File False
set supybot.plugins.ChanLog.SQLAlchemy True
set supybot.plugins.ChanLog.SQLAlchemy.URI <Your DB URI>

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
