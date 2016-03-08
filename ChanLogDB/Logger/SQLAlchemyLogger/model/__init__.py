from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, types
from constants import *

metadata = MetaData()

channels = Table('channel', metadata,
     Column('id', types.Integer, primary_key=True),
     Column('name', types.Unicode(32)),
     Column('network', types.Unicode(32)),
     Column('num_lines', types.Integer)
 )

logs = Table('log', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('channel_id', types.Integer, ForeignKey("channel.id"), 
           nullable=False),
    Column('created_on', types.DateTime, index=True),
    Column('type', types.Integer),
    Column('nick', types.Unicode(40)),
    Column('text', types.UnicodeText())
)