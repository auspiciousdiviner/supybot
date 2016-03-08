def getLogger( config ):
	"""Find out which logger we want to use and return a factory that can create logs"""
	if config.registryValue( 'SQLAlchemy' ):
		from SQLAlchemyLogger import SQLAlchemyLogFactory as LogFactory
	elif config.registryValue( 'File' ):
		from FileLogger import FileLogFactory as LogFactory
	else:
		from BaseLogger import BaseLogFactory as LogFactory
	return LogFactory(config)
	