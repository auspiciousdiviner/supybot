
 
from sqlobject import *
class Channel(SQLObject):
    network = StringCol(length=32) #network name
    name = StringCol(length=32) # channel name
    def _set_name(self, name):
        name = name.lstrip('#') # remove # in the channel name
        self._SO_set_name(name)
    num_lines = BigIntCol(default=0) #some statistics if you care to update these
    lpd_now = FloatCol(default=0) 
    lpd_past = FloatCol(default=0)
    serverIndex = DatabaseIndex(network, name, unique= True)
    logs = MultipleJoin('Log', orderBy='date')

# db scheme for the actual logs
class Log(SQLObject):
    channel = ForeignKey('Channel', cascade=True)
    created_on = DateTimeCol()
    type = StringCol(length=20)
    nick = StringCol(length=32)
    #text = StringCol() 
    text = UnicodeCol()
    created_on_index = DatabaseIndex( created_on )

