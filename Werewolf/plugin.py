###
# Copyright (c) 2010, Julian Aloofi
# All rights reserved.
#
#    This file is part of supybot-werewolf.
#
#    supybot-werewolf is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    supybot-werewolf is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with supybot-werewolf.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import random, threading, pickle, os


class Werewolf(callbacks.Plugin):
    """This plugin lets you play the werewolf game also known as mafia.
    To start a game use the 'startgame' command. Now the minimum number
    of players (default 3) needs to join the game with 'joingame'.
    Then the player who called 'startgame' can use 'begingame' to start the round.
    You can use 'tellrules' to let the bot give users a link
    to the game rules.
    """
    threaded = True
    
    #has the join already started?
    join_started = False
    #has the game already started?
    game_started = False
    #includes all players
    playerlist = []
    bots = 0
    #wolves, seers, villagers
    villagers = []
    wolves = []
    seer = ""
    shooter = ""
    #what phase are we currently in? 'morning', 'discussion' or 'night'?
    game_phase = ""
    #in which channel is the game running?
    gamechannel = ""
    #how many votes does a kill
    list_of_death = []
    #who voted yet?
    already_voted = []
    # a thread to move on
    move_on = False
    #saves the current scores
    channelscores = {}
    #villagers which can't vote anymore
    wounded_villagers = []
    #marks if shooter shot or seer revealed
    shooter_shot = False
    seer_saw = False

    
    seer_intro = ("You are the seer! You have been granted great insight to discover the true intentions of each player. After every night you can find out "+
            "what the real identity of a player is. Try to keep your "+
            "own identity secret or the werewolves will most likely "+
            "kill you in the night. You can try to lead the discussion into "+
            "the right direction though. Apart from your abilities to "+
            "reveal other players identities you are a normal villager and will "+
            "only win if the villagers win.")
            
    werewolves_intro = ("You are a werewolf! Your beastly blood allows you to transform into a terrifying hybrid of Man and Wolf. Don't tell anybody! "+
            "You have to kill all villagers. Hide your identity in "+
            "the public votings and act like a normal villager. "+
            "In the night you will get an opportunity to kill villagers "+
            "together with other werewolves in a private voting. "+
             "Currently werewolves are: ")
            
    villagers_intro = ("You are a villager. What cruel luck to be preyed upon by the werewolves of the night! You will have to discuss "+
            "with the other villagers during the daytime and try to find "+
            "out who the werewolves are before they get aquainted with you. After each discussion period, "+
            "you and the other players will vote for "+
            "a player to be killed in the middle of the village square. Try to find out who the "+
            "werewolves are without making yourself suspect.")
            
    shooter_intro = ("You are the shooter. Given an old rifle used by your grandpa in the old WW2, you use it to carry out vigilante justice in your village. You can shoot at another player "+
            "every morning. If you hit a villager, he is wounded and can't "+
            "vote in the public elections anymore. If you hit a werewolf or the seer, they will die. "+
            "Therefore, it may be wise to choose to not shoot anyone at all. "+
            "You are a normal villager apart from that, and will only win if "+
            "the villagers win.")
    
    def __init__(self, irc):
        self.__parent = super(Werewolf, self)
        self.__parent.__init__(irc)
        self._cleanup()

        
    def _cleanup(self):
        """cleans all variables up"""
        if self.move_on != False:
            self.move_on.cancel()
        self.move_on = False
        self.join_started = False
        self.game_started = False
        self.playerlist = []
        self.bots = 0
        self.villagers = []
        self.wolves = []
        self.seer = ""
        self.shooter = ""
        self.game_phase = ""
        self.gamechannel = ""
        self.list_of_death = []
        self.already_voted = []
        self.wounded_villagers = []
        self.shooter_shot = False
        self.seer_saw = False
        
    def _write_scores(self):
        for player in self.playerlist:
            if not player in self.channelscores:
                self.channelscores[player] = 1
            else:
                self.channelscores[player] += 1
            #additional points for wolves
            if player in self.wolves:
                self.channelscores[player] += 2
        outputfile = open(self.gamechannel+".scores", "wb")
        pickle.dump(self.channelscores, outputfile)
        outputfile.close()
        
    def _read_scores(self, msg):
        if os.path.isfile(msg.args[0]+".scores"):
            inputfile = open(msg.args[0]+".scores", "rb")
            self.channelscores = pickle.load(inputfile)
            inputfile.close()
        
    def listscores(self, irc, msg, args):
        """takes no arguments
        
        Tells the score list for the current channel"""
        if not self.channelscores:
            self._read_scores(msg)
        #w00t that's a use of lambda, buzzword attack!
        scores = sorted(self.channelscores.iteritems(), key=lambda (k,v):(v,k), reverse=True)
        msgstring = ""
        for item in scores:
            msgstring += " : ".join(map(str, item))+", "
        if msgstring != "":
            irc.reply(msgstring)
        else:
            irc.reply("There are not any scores for this channel yet.")

        
    listscores = wrap(listscores)
        
    def start(self, irc, msg, args):
        """takes no arguments
        
        Starts the game and allows other players to join with 'joingame'.
        """
        if not self.join_started and not self.game_started:
            #clear the player list
            self.playerlist = []
            #remember the game channel
            self.gamechannel = msg.args[0]
            self._read_scores(msg)
            irc.reply(
            "A new game of Werewolf has started! To join use "+
            "the 'joingame' command. To start the game, use 'begingame'.", 
            prefixNick=False, private=False, to=self.gamechannel)
            #irc.reply(
            #"If you don't know the rules yet, check them out "+
            #"with the 'tellrules' command", prefixNick=False, private=False,
            #to=self.gamechannel)
            self.playerlist.append(msg.nick)
            irc.reply("added " + msg.nick + " to the player list.", action=True
            ,private=False, to=self.gamechannel)
            #join_started is there to track the current state of joining
            self.join_started = True
        else:
            irc.reply("A game has already been started or is running!")

    start = wrap(start)
    
    def addbot( self, irc, msg, args ):
    
        irc.reply("Bot added", to=self.gamechannel)
        self.bots = self.bots + 1
    
    addbot = wrap(addbot)
    
    def removebot( self, irc, msg, args ):
    
        if self.bots <= 0:
            irc.reply("You can not have a negative number of bots playing!", to=self.gamechannel)
            
        else:
            self.bots = self.bots + 1
    
    removebot = wrap(removebot)

    def tellrulesto(self, irc, msg, args, nickname):
        """<nickname>
        
        Tells <nickname> the rules"""
        irc.reply(
        "You can find the rules at http://www.eblong.com/zarf/werewolf.html",
        to=nickname, private=False)

    tellrulesto = wrap(tellrulesto, ['text'])
    
    
    def leave(self, irc, msg, args):
        """takes no arguments
        
        allows the caller to leave the game"""
        if msg.nick in self.playerlist:
            self.playerlist.remove(msg.nick)
            if self.game_started == False:
                return
            if msg.nick in self.villagers:
                self.villagers.remove(msg.nick)
                irc.reply(msg.nick+" has left the game before the werewolves could get to him!. He was a villager...",
                to=self.gamechannel, prefixNick=False)
                if msg.nick in self.wounded_villagers:
                    self.wounded_villagers.remove(msg.nick)
            elif msg.nick in self.wolves:
                self.wolves.remove(msg.nick)
                irc.reply(msg.nick+" has left the game to repent for his evil deeds. He was a werewolf!",
                to=self.gamechannel, prefixNick=False)
            elif msg.nick == self.seer:
                self.seer == ""
                irc.reply(msg.nick+" has left the game, leaving you all alone to decide the fate of your village without his insight. He was the prophetic Seer!",
                to=self.gamechannel, prefixNick=False)
            elif msg.nick == self.shooter:
                self.shooter == ""
                irc.reply(msg.nick+" has left the game to go clean his gun. He was the shooter!",
                to=self.gamechannel, prefixNick=False)
            if not self._check_continue(irc, msg, args):
                if self.game_phase == "discussion":
                    if len(self.already_voted) == len(self.playerlist)-len(self.wounded_villagers):
                        self._phase_night(irc, msg, args)
                        return
    
    leave = wrap(leave)
    
    def doPart(self, irc, msg):
        if msg.nick in self.playerlist:
            self.leavegame(irc, msg, 0)
            
    def doQuit(self, irc, msg):
        if msg.nick in self.playerlist:
            self.leavegame(irc, msg, 0)
    
    def doNick(self, irc, msg):
        if msg.nick in self.playerlist:
            self.playerlist[self.playerlist.index(msg.nick)] = msg.args[0]
        if msg.nick in self.villagers:
            self.villagers[self.villagers.index(msg.nick)] = msg.args[0]
        if msg.nick in self.wolves:
            self.wolves[self.wolves.index(msg.nick)] = msg.args[0]
        if msg.nick == self.seer:
            self.seer = msg.args[0]
        if msg.nick == self.shooter:
            self.shooter = msg.args[0]
        if msg.nick in self.list_of_death:
            self.list_of_death[self.list_of_death.index(msg.nick)] = msg.args[0]
        if msg.nick in self.already_voted:
            self.already_voted[self.already_voted.index(msg.nick)] = msg.args[0]
        if msg.nick in self.wounded_villagers:
            self.wounded_villagers[self.wounded_villagers.index(msg.nick)] = msg.args[0]
        
    
    def tellrules(self, irc, msg, args):
        """takes no arguments
        
        Tells the caller the rules"""
        irc.reply(
        "You can find the rules at http://www.eblong.com/zarf/werewolf.html")
        
    tellrules = wrap(tellrules)
    
    def join(self, irc, msg, args):
        """takes no arguments
        
        Allows players to join the game."""
        if msg.nick == "nobody":
            irc.reply("You can't call yourself nobody in this game. "+
            "Also, another name is surely great for your self-confidence. Change your nickname!")
            return
        if not self.game_started and self.join_started:
            if not msg.nick in self.playerlist:
                #add command caller to the player list
                self.playerlist.append(msg.nick)
                #and tell that to the IRC
                irc.reply("added " + msg.nick + " to the player list."
                ,action=True, private=False, to=self.gamechannel)
                 
            else:
                irc.reply("You have already joined the game!")
        elif self.game_started and not self.join_started:
            irc.reply("I am terribly sorry, the game has already started. Please wait until "+
            "a new round starts.")
        else:
            irc.reply("Nobody started a round yet. Use the 'startgame' "+
            "command to start a new round!")
    
    join = wrap(join)
    
    def listplayers(self, irc, msg, args):
        """takes no arguments
        
        Lists all players still playing"""
        if self.game_started or self.join_started:
            msgstring = "Players currently playing: " + self._get_playerlist()
            irc.reply(msgstring)
        
    listplayers = wrap(listplayers)
    
    def _get_playerlist(self):
        return ", ".join(map(str, self.playerlist))
        
    def whatami(self, irc, msg, args):
        """takes no arguments
        
        Tells the caller what he is."""
        if self._check_start(irc, msg, args): return
        if msg.nick in self.villagers:
            irc.reply(self.villagers_intro, private=True, to=msg.nick)
        elif msg.nick in self.wolves:
            irc.reply(self.werewolves_intro+
            " ".join(map(str, self.wolves)), private=True, to=msg.nick)
        elif msg.nick == self.seer:
            irc.reply(self.seer_intro, private=True, to=msg.nick)
        elif msg.nick == self.shooter:
            irc.reply(self.shooter_intro, private=True, to=msg.nick)
            
    whatami = wrap(whatami)
    
    def begin(self, irc, msg, args):
        """takes no arguments
        
        Begins the round after a 'startgame'"""

        if not self.join_started:
            irc.reply("You need to start a game using 'startgame' first!")
            return
        if self.game_started:
            irc.reply("Game already started!")
            return
            
        if len(self.playerlist) < 3:
            irc.reply("There are not enough players to start the game. "+
            "You need at least 3 players to start the game, due to how impossible it is to play with this few players.")
            return
        else:
            #join phase is over
            self.join_started = False
            self.game_started = True
            #tell everyone the game is starting
            irc.reply(ircutils.bold("Night is falling, "+
            "and the game is starting! "+
            "I am telling everyone their roles now. ")
            +"If you're using an IRC client like irssi you may want to "+
            "\"/unignore *\" to receive private messages. "+
            "Whenever I'm asking you to do something, "+
            ircutils.bold("*privately*")+" /msg me "+
            "to issue the command.",
            prefixNick=False, private=False, to=self.gamechannel)
            ##assign the roles##
            #randomize player list order:
            random.shuffle(self.playerlist)
            if len(self.playerlist) < 6:
                self.seer = self.playerlist[0]
                self.wolves.append(self.playerlist[1])
                self.villagers.extend(self.playerlist[2:])
            elif len(self.playerlist) < 7:
                self.seer = self.playerlist[0]
                self.shooter = self.playerlist[1]
                self.wolves.append(self.playerlist[2])
                self.villagers.extend(self.playerlist[3:])
            elif len(self.playerlist) < 11:
                self.seer = self.playerlist[0]
                self.shooter = self.playerlist[1]
                self.wolves.extend(self.playerlist[2:4])
                self.villagers.extend(self.playerlist[4:])
            elif len(self.playerlist) < 15:
                self.seer = self.playerlist[0]
                self.shooter = self.playerlist[1]
                self.wolves.extend(self.playerlist[2:5])
                self.villagers.extend(self.playerlist[5:])
            elif len(self.playerlist) < 20:
                self.seer = self.playerlist[0]
                self.shooter = self.playerlist[1]
                self.wolves.extend(self.playerlist[2:6])
                self.villagers.extend(self.playerlist[6:])
            else:
                self.seer = self.playerlist[0]
                self.shooter = self.playerlist[1]
                self.wolves.extend(self.playerlist[2:7])
                self.villagers.extend(self.playerlist[7:])
            #sort, so nobody can abuse 'listusers'
            self.playerlist.sort()
            #tell everyone what he is
            irc.reply(self.seer_intro, private=True, to=self.seer)
            if len(self.playerlist) > 6:
                irc.reply(self.shooter_intro, private=True, to=self.shooter)
                
            for player in self.wolves:                        
                irc.reply(self.werewolves_intro+
                " ".join(map(str, self.wolves)), private=True, to=player)
            for player in self.villagers:
                irc.reply(self.villagers_intro, private=True, to=player)
            irc.reply("Okay, all players know their roles now. "+
            ircutils.bold("Don't tell anyone what you are!")+
            " The game is starting now!", prefixNick=False)
            irc.reply("Welcome to a new round of werewolf! "
            +"This game is a "+
            "game of accusations, lying, bluffing, second-guessing, "+
            "assassination, and mob hysteria. All players seem to be normal "+
            "villagers, but we have "+str(len(self.wolves))+
            " werewolves hidden in our village. "+
            "Try to find out who the werewolves are, or get eaten in the darkness of the "+
            "night.", to=self.gamechannel, prefixNick=False)
            self._phase_morning(irc, msg, args)

    begin = wrap(begin)
             
    def _game_over(self, irc, msg, args):
        irc.reply("The game is over!", to=self.gamechannel, prefixNick=False)
        if len(self.wolves) == 0:
            irc.reply("The villagers have won! Let's rejoice for the survival of our village!", to=self.gamechannel,
            prefixNick=False)
        else:
            irc.reply("The werewolves have won! Oh woe is the villagers, all made food of their fellow villagers possessed by the Will of the Beast of the Night.", to=self.gamechannel,
            prefixNick=False)
            for player in self.playerlist:
                if player in self.villagers:
                    self.villagers.remove(player)
                    self.playerlist.remove(player)
                    if player in self.wounded_villagers:
                        self.wounded_villagers.remove(player)
                elif player == self.seer:
                    self.seer == ""
                    self.playerlist.remove(self.seer)
                elif player == self.shooter:
                    self.shooter == ""
                    self.playerlist.remove(self.shooter)
        irc.reply("Players still alive: " + self._get_playerlist(),
        to=self.gamechannel, prefixNick=False)
        self._write_scores()
        self._cleanup()
        
    def _phase_discuss(self, irc, msg, args):
        self.game_phase = "discussion"
        if self.move_on != False:
            self.move_on.cancel()
        self.move_on = False
        irc.reply("It is time to discuss now! The public forum is open! "+
        "Who could the werewolves be? If you have a suspicion, use the "+
        ircutils.bold("'votekill'")+
        " command to vote for the death of your suspect!",
        to=self.gamechannel, private=False)
        self.list_of_death = []
        self.already_voted = []
        
    def votekill(self, irc, msg, args, nickname):
        """<nickname>
        
        Votes to kill <nickname>"""
        if self._check_start(irc, msg, args): return
        if self.game_phase != "discussion" and self.game_phase != "night" and self.game_phase != "morning":
            irc.reply("This command can't be used right now!")
            return
        if msg.nick in self.already_voted:
            irc.reply("You already gave a vote for the current voting!")
            return
        if msg.nick in self.wounded_villagers:
            irc.reply("You are wounded and cannot vote!")
            return
        if not nickname in self.playerlist:
            if not self.game_phase == "morning" and not nickname == "nobody":
                irc.reply(nickname+" is not participating in this round.")
                return
        #discussion mode:
        if self.game_phase == "discussion":
            self.already_voted.append(msg.nick)
            if not nickname in self.list_of_death:
                self.list_of_death.append(nickname)
                self.list_of_death.append(1)
            else:
                self.list_of_death[self.list_of_death.index(nickname)+1] =(
                self.list_of_death[self.list_of_death.index(nickname)+1] + 1)
            #irc.reply(msg.nick+" voted to kill "+nickname+
            #".", to=self.gamechannel, prefixNick=False)
            if len(self.already_voted) == len(self.playerlist)-len(self.wounded_villagers):
                self._phase_night(irc, msg, args)
                return
            else:
                irc.reply(msg.nick+" voted to kill "+nickname+
                ". There still are "+str(len(self.playerlist)-
                len(self.already_voted)-len(self.wounded_villagers))+" votes missing.",
                 to=self.gamechannel,
                prefixNick=False)
                if len(self.playerlist)/2 < len(self.already_voted)+1+len(self.wounded_villagers) and (
                self.move_on == False):
                    irc.reply("The majority of votes are in! "+
                    "You have two minutes left to vote!", to=self.gamechannel,
                    private=False, prefixNick=False)
                    self.move_on = threading.Timer(120, self._vote_countdown,
                    [irc, msg, args])
                    self.move_on.start()
                    return
        #night mode:
        if self.game_phase == "night":
            if not msg.nick in self.wolves:
                return
            self.already_voted.append(msg.nick)
            if not nickname in self.list_of_death:
                self.list_of_death.append(nickname)
                self.list_of_death.append(1)
            else:
                self.list_of_death[self.list_of_death.index(nickname)+1] =(
                self.list_of_death[self.list_of_death.index(nickname)+1] + 1)
            for wolf in self.wolves:
                if msg.nick != wolf: 
                    irc.reply(ircutils.bold(msg.nick+" voted to kill "
                    +nickname+"."), to=wolf, private=True)
            if len(self.already_voted) == len(self.wolves):
                self._wolf_poll_finished(irc, msg, args)
                return
        #morning phase (for the shooter):
        if self.game_phase == "morning":
            if not msg.nick == self.shooter:
                return
            #shoot nobody
            if nickname == "nobody":
                irc.reply("The shooter decided to shoot nobody, he had to reloaded his gun.", to=self.gamechannel,
                prefixNick=False)
                self.shooter_shot = True
                if self.seer_saw == True or self.seer == "":
                    self._phase_discuss(irc, msg, args)
                return
            #make a ~33% accuracy
            randval = random.randint(0, 2)
            if randval != 1:
                irc.reply("The shooter's shot missed its target!", prefixNick=False,
                to=self.gamechannel)
                self.shooter_shot = True
                irc.reply("Your shot missed!", to=self.shooter, private=True)
                if self.seer_saw == True or self.seer == "":
                    self._phase_discuss(irc, msg, args)
                return
            if nickname in self.wolves:
                self.wolves.remove(nickname)
                self.playerlist.remove(nickname)
                irc.reply("The shooter decided to shoot at "+nickname+". "+
                nickname+" was a werewolf and is dead now!", to=self.gamechannel)
                irc.reply("You are dead now, sorry.", to=nickname, private=True)
            elif nickname in self.villagers:
                if nickname in self.wounded_villagers:
                    self.wounded_villagers.remove(nickname)
                irc.reply("The shooter decided to shoot at "+nickname+". "+
                nickname+" was a villager and can't vote anymore now.",
                to=self.gamechannel)
                self.wounded_villagers.append(nickname)
            elif nickname == self.seer:
                self.seer == ""
                self.playerlist.remove(nickname)
                irc.reply("The shooter decided to shoot at "+nickname+". "+
                nickname+" was the seer, and is dead now! Good luck villagers! No more great wisdom from the Seer! He will be mourned!", to=self.gamechannel)
                irc.reply("You are dead now, sorry.", to=nickname, private=True)
                self._phase_discuss(irc, msg, args)
            elif nickname == self.shooter:
                self.shooter == ""
                self.playerlist.remove(nickname)
                irc.reply("The shooter shot himself! Looks like "+nickname+
                " had serious problems.", to=self.gamechannel)
                irc.reply("You are dead now, sorry.", to=nickname, private=True)
            self.shooter_shot = True
            if self._check_continue(irc, msg, args) == True:
                return
            if self.seer_saw == True or self.seer == "":
                self._phase_discuss(irc, msg, args)
                
                     
    lynch = wrap(votekill, ['text'])
    shoot = wrap(votekill, ['text'])
    votekill = wrap(votekill, ['text'])
    kill = wrap(votekill, ['text'])
    
    
    def _vote_countdown(self, irc, msg, args):
        #to be used as threaded function
        if self.game_phase == "discussion":
            self._phase_night(irc, msg, args)
            
    def _seer_countdown(self, irc, msg, args):
        #to be used as threaded function
        if self.game_phase == "morning":
            irc.reply("The sun is risen, and everyone finished their breakfast.",
            to=self.gamechannel, prefixNick=False)
            self._phase_discuss(irc, msg, args)
            
    def _wolf_poll_finished(self, irc, msg, args):
        self.game_phase="nightannounce"
        self.move_on.cancel()
        self.move_on = False
        irc.reply("All werewolf votes are in!"
        ,to=self.gamechannel, prefixNick=False)
        if len(self.list_of_death) > 0:
            self._kill_someone_now(irc, msg, args)
        
        self.list_of_death = []
        self.already_voted = []
        
        self._phase_morning(irc, msg, args)
    
    def _phase_night(self, irc, msg, args):
        self.game_phase="voteannounce"
        if self.move_on != False:
            self.move_on.cancel()
        self.move_on = False
        irc.reply("Voting has finished!"
        ,to=self.gamechannel, prefixNick=False)
        self._kill_someone_now(irc, msg, args)
        self.list_of_death = []
        self.already_voted = []
        
        if self._check_continue(irc, msg, args) == True:
            return
        
        self.game_phase="night"
        irc.reply("Night is falling! Watch out, because the werewolves "+
        "have the opportunity to kill one of you now! ", to=self.gamechannel,
        prefixNick=False, private=False)
        for wolf in self.wolves:
            irc.reply("You and the other wolves "+
            "can kill someone now. Vote to kill someone by "+
            ircutils.bold("*privately*")+" telling me your victim with "+
            "the 'votekill' command. You only have "+
            "two minutes before sun rise.", private=True, to=wolf)
            
        if self.move_on == False:
            self.move_on = threading.Timer(120, self._wolf_poll_finished,
            [irc, msg, args])
            self.move_on.start()
    
    def _kill_someone_now(self, irc, msg, args):
        highestcount = 0
        deathplayer = ""
        is_draw = False
        for item in self.list_of_death:
            if isinstance(item, int):
                if item > highestcount:
                    highestcount = item
                    deathplayer = (
                    self.list_of_death[self.list_of_death.index(item)-1])
                    is_draw = False
                elif item == highestcount:
                    is_draw = True
        if self.game_phase == "voteannounce":
            if is_draw == True:
                irc.reply("There was a draw in the election! Nobody will be "
                "killed.",
                to=self.gamechannel, prefixNick=False)
                return
            else:
                irc.reply(ircutils.bold(
                "The villagers have decided to kill "+deathplayer+
                " with "+str(highestcount)+" votes."), to=self.gamechannel, 
                prefixNick = False)
                if not deathplayer in self.playerlist:
                    irc.reply(deathplayer+" has left the game before the "+
                    "election finished. Nobody will be killed. ",
                    to=self.gamechannel, prefixNick=False)
                    return
        elif self.game_phase == "nightannounce":
            if is_draw == True:
                irc.reply("The werewolves couldn't decide on a player to kill"+
                ". Everyone is still alive.",to=self.gamechannel,
                prefixNick=False)
                return
            else:
                irc.reply(ircutils.bold(
                "The werewolves have decided to kill "+deathplayer+
                " with "+str(highestcount)+" votes."), to=self.gamechannel, 
                prefixNick = False)
                if not deathplayer in self.playerlist:
                    irc.reply(deathplayer+" ran away before the "+
                    "werewolves could get him. Nobody will be killed. ",
                    to=self.gamechannel, prefixNick=False)
                    return
        if deathplayer in self.villagers:
            irc.reply(deathplayer+" was a villager.", to=self.gamechannel,
            prefixNick=False)
            self.villagers.remove(deathplayer)
            if deathplayer in self.wounded_villagers:
                self.wounded_villagers.remove(deathplayer)
        elif deathplayer in self.wolves:
            irc.reply("Congratulations! "+deathplayer+" was a werewolf!",
             to=self.gamechannel,
            prefixNick=False)
            self.wolves.remove(deathplayer)
        elif deathplayer == self.seer:
            irc.reply("Oh no! "+deathplayer+" was the seer!", 
            to=self.gamechannel,
            prefixNick=False)
            self.seer = ""
        elif deathplayer == self.shooter:
            irc.reply(deathplayer+" was the shooter.", to=self.gamechannel,
            prefixNick=False)
            self.shooter = ""
        irc.reply("You are dead now, sorry.", to=deathplayer, private=True)
        self.playerlist.remove(deathplayer)
        self.list_of_death = []
        self.already_voted = []
            
            
    def _check_start(self, irc, msg, args):
        """checks whether a user is allowed to issue commands"""
        if not msg.nick in self.playerlist:
            irc.reply("You're not participating in the game.")
            return True
        if not self.game_started:
            irc.reply("Someone needs to start a game using 'startgame' first.")
            return True
        return False
        
    def _phase_morning(self, irc, msg, args):
        self.game_phase = "morning"
        #just to be sure.. :D
        self.list_of_death = []
        self.already_voted = []
        self.shooter_shot = False
        self.seer_saw = False
        seerval = 0
        if self.seer != "":
            seerval = 1
        shooterval = 0
        if self.shooter != "":
            shooterval = 1
        if self._check_continue(irc, msg, args) == True:
            return
        #start the countdown
        self.move_on = threading.Timer(90, 
        self._seer_countdown, [irc, msg, args])
        self.move_on.start()
        if seerval == 0 and shooterval == 0:
                irc.reply("The sun is rising and a new day "
                +"begins. "+
                "Unfortunately the seer is dead.",
                prefixNick=False, to=self.gamechannel)
                self._phase_discuss(irc, msg, args)
                return
        elif seerval == 0 and shooterval == 1:
                irc.reply("The sun is rising and a new day begins. "+
                "The seer is dead, but the shooter has the opportunity to "+
                "shoot someone now.", to=self.gamechannel, prefixNick=False)
        elif seerval == 1 and shooterval == 1:
            irc.reply("The sun is rising and a new day begins. The seer has "+
            "the opportunity to reveal another players identity now and the "+
            "shooter can shoot someone.", 
            prefixNick=False, to=self.gamechannel)
        elif seerval == 1 and shooterval == 0:
            irc.reply("The sun is rising and a new day begins. The seer has "+
            "the opportunity to reveal another players identity now.",
            to=self.gamechannel, prefixNick=False)
        if seerval == 1:
            irc.reply("You can reveal the identity of another player now. "+
            "To do that, "+ircutils.bold("*privately*")+
            " tell me which player you'd like "+
            "to identify with 'reveal NAME_OF_PLAYER', e.g. 'reveal "+
            "John"+"' "+
            "to reveal '"+"John"+"'s identity", private=True, to=self.seer)
        if shooterval == 1:
            irc.reply("You can shoot another player now. "+
            "To do that, "+ircutils.bold("*privately*")+
            " tell me which player you'd like to shoot with 'votekill NAME_OF_PLAYER'"+
            ", e.g. 'votekill "+"John"+"' to shoot at '"+"John"+
            ". You can also choose to not shoot anyone with 'votekill nobody'", to=self.shooter,
            private=True, prefixNick=False)
        
    def _check_continue(self, irc, msg, args):
        """Checks whether the game is over"""
        seerval = 0
        if self.seer != "":
            seerval = 1
        shooterval = 0
        if self.shooter != "":
            shooterval = 1
        if len(self.villagers)+seerval+shooterval <= len(self.wolves) or len(
        self.wolves)==0:
            self._game_over(irc, msg, args)
            return True
        return False
            
        
    def reveal(self, irc, msg, args, nickname):
        """<nickname>
        
        Reveals the identity of <nickname> to the seer"""
        if self._check_start(irc, msg, args): return
        if self.game_phase != "morning":
            return
        if msg.nick != self.seer:
            return
        if not nickname in self.playerlist:
            irc.reply(nickname+" is not playing in this round.",
            to=self.seer, private=True)
            return
        if nickname in self.villagers:
            irc.reply(nickname+" is a villager!", private=True
            , to=self.seer)
            irc.reply("The seer has revealed the identity of a "+
            "villager.", private=False, prefixNick=False, 
            to=self.gamechannel)
        if nickname in self.wolves:
            irc.reply(nickname+" is a werewolf!", private=True
            , to=self.seer)
            irc.reply("The seer has revealed the identity of a "+
            "werewolf!", private=False, prefixNick=False, 
            to=self.gamechannel)
        if nickname == self.seer:
            irc.reply("You can't reveal your own identity!", private=True,
            to=self.seer)
            return
        if nickname == self.shooter:
            irc.reply(nickname+" is the shooter!", private=True, to=self.seer)
            irc.reply("The seer has revealed the identity of the shooter.",
            private=False, prefixNick=False, to=self.gamechannel)
        self.seer_saw = True
        if self.shooter_shot == True or self.shooter == "":
            self._phase_discuss(irc, msg, args)
        
    reveal = wrap(reveal, ['text'])
        

Class = Werewolf


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
