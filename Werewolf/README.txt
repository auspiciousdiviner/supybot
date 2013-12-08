This plugin moderates and leads a game of werewolf.
Project home is at https://launchpad.net/supybot-werewolf
You can also report bugs over there.


=== HOW TO GET THE BOT RUNNING ===
This bot works as a plugin for supybot. To use it, you have to install supybot first.
Supybot comes with any distribution I know, you should use your distro's package.
To set up the bot, create an empty directory, and in this directory create an empty
folder called "plugins". If you decide to name your empty directory "werewolf", you would
have a similar folder structure:

	/home/user/werewolf/plugins/

Move the "Werewolf" folder to the plugins directory. (the folder you unpacked
from the .tar.gz along with the COPYING file)
Now run supybot-wizard in the directory you created(/home/user/werewolf in this example). Just follow the
instructions on the screen to set it up. When it comes to
"Would you like to look at plugins individually?", you can select the game as "Werewolf".
Note that it is handy to define a prefix for the bot when playing, like ! or @, so any messages
that start with ! or @ get interpreted as commands (and you don't have to say the bot's name all the time).
After going through all the steps, you should have a directory strcuture similar to

	/home/user/werewolf/data/
	/home/user/werewolf/conf/
	/home/user/werewolf/logs/
	/home/user/werewolf/backup/
	/home/user/werewolf/plugins/
	/home/user/werewolf/plugins/Werewolf/
	/home/user/werewolf/bot_name.conf

Also, after playing, the bot will create files called <channelname>.scores.
This file stores the channel scores. You can look at them with 'listscores'.
If you're planning to run the bot on Freenode/OFTC, or have problems
with the flooding control of your chat network, read the
"Note for Freenode/OFTC users" section below.



=== Command overview ===
The following commands are possible to interact with the bot:

listscores:	Lists the current scores of all players playing. Players get
			1 point when winning as villager, and 3 points when winning as werewolf.

startgame:	The player who calls this function first starts the game. Players can join
			the game now.

joingame:	After someone has called 'startgame', players can join the game with this command.

begingame:	The player who called 'startgame' this round can use this command to start the game
			once at least 2 players joined the game (so there are 3 players playing).

listplayers:	Lists the players who currently participate in the game.

votekill <someone>:	Allows the player who used the command to vote for the death of
					<someone> in the current election. Also, allows the shooter to shoot someone.

reveal <someone>:	If the player who used the command is the seer, he can reveal
					the identity of <someone> in the morning.

tellrules:	Tells the player who used the command the rules.

tellrulesto <someone>:	Tells <someone> the rules.

leavegame:	Allows the player who called the function to leave the game.

whatami:	Tells the called privately what role he has.



=== RULES ===
This is a short summary of the game rules. You can read a more lenghty version
of the rules online at http://www.eblong.com/zarf/werewolf.html
This game requires at least 3 players to run.

== The game phases ==
The game is divided into three phases:

# The morning phase:
    In this phase, the seer can reveal the identity of another player.
    The shooter can shoot at another player.
    All other players have to wait while this is happening.
    The seer and shooter will get their instructions privately by the game bot.

# The election phase:
    After the morning phase comes the election phase. All players can vote
    for a suspect they'd like to kill now. They can do that publicly with the
    'votekill' command. After everyone has finished voting, the player with the
    most votes will be killed, and his role will be revealed.
    
# The night phase:
    After the election phase comes the night phase. In this phase, the werewolves
    privately talk to each other and try to decide on someone to kill.
    They use the 'votekill' command as well.

== The player roles ==
The following roles will be assigned to the players:

# Villager:
    That's the normal role. The villagers just vote in the election phase
    and don't have much more to do. They win if all werewolves are killed.
    
# Werewolf:
    The werewolves try to behave like they are normal villagers. They can vote
    in the public elections as well, but additionally privately vote in the night
    to kill another player. They win if the number of villagers is equal or less
    than their own. The more villagers there initially are,
    the more werewolves will be there.
    
# Seer:
    The seer is a normal villager, with one excpetion: He can reveal the identity
    of another player every morning. This makes him a target for the werewolves,
    but also a strong ally for the villagers. There will always only be one
    seer in each game.
    
# Shooter:
    The shooter is a normal villager, with one exception: He can shoot at another
    player every morning. If he hits a villager, the villager will not be able to
    vote anymore. The shooter has a 33% chance to hit.
    verIf he hits a werewolf or the seer, they will die. The shooter
    can choose not to shoot anyone with 'votekill nobody'. There will
    always only be one shooter in each game. You need at least 6 players to play
    with the shooter.




=== Note for Freenode/OFTC users ===
If the bot gets kicked because of flooding ("Excess Flood") try
to increase supybots throttle time with:
config supybot.protocols.irc.throttleTime 2.0

(If you don't know supybot well enough to know how to execute that, just
change the supybot.protocols.irc.throttleTime in the bot's .conf file)

2.0 is a value that works for freenode, 1.0 is the default value. It represents
the time between messages sent by the bot.



Please also note that currently it probably is not possible to play in more
than one channel at the same time. If you want to run the bot in many
channels at once please create different supybot configurations.

If you need any further help setting the game up, ask on
https://answers.launchpad.net/supybot-werewolf or send me a mail to
julian.fedora %AT& googlemail.com
