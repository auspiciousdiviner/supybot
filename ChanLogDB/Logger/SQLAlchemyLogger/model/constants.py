MESSAGE = 0
ACTION = 1
NICKCHANGE = 2
NOTICE = 3
MODE = 4
TOPIC = 5
JOIN = 6
KICK = 7
PART = 8
QUIT = 9


sql = """
UPDATE log SET type = 0 where type='message';
UPDATE log SET type = 1 where type='action';
UPDATE log SET type = 2 where type='nickchange';
UPDATE log SET type = 3 where type='notice';
UPDATE log SET type = 4 where type='mode';
UPDATE log SET type = 5 where type='topic';
UPDATE log SET type = 6 where type='join';
UPDATE log SET type = 7 where type='kick';
UPDATE log SET type = 8 where type='part';
UPDATE log SET type = 9 where type='quit';
"""