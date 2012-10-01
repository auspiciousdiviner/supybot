from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.callbacks as callbacks

import poker
reload(poker)

class Player:
    def __init__(self,name,stack=1000):
        self.name = name
        self._stack = stack
        self._hand = []

    def bet(self, amount):
        if amount <= self._stack:
            self._stack -= amount
            return True
        else:
            return False

    def deal_to(self,card):
        self._hand.append(card)

    def tell_hole_cards(self):
        holecards = " ".join([poker.GetCard(c) for c in self._hand])
        irc.queueMsg(ircmsgs.privmsg(self.name, holecards))


PREDEALT=0
PREFLOP=1
FLOP=2
TURN=3
RIVER=4
SHOWDOWN=5
READYDEAL=-1

class Game:
    def __init__(self, chan):
        self._chan = chan
        self._board = []
        self._pot = {'main':0}
        self._players = []  # permanent list of players sitting at table
        self._blinds = (20,10) 
        self._bet = 0
        self._state = PREFLOP
        self._order = []    # build this list for each round to know in what
                            # order who bets, etc.  last player is dealer
        self._action = 0    # index of player who's the "action"

    def deal(self,irc,msg,args):
        if self._action != READYDEAL:
            irc.reply("Not ready to deal yet. Hold on there, sparky")
            return
        if self._state == PREDEALT:
            deck=poker.ShuffleDeck()
            self._board = poker.Deal(deck, 5)
            # create the visible board
            self._visboard = []
            # I could just deal both at the same time, but this feels better 
            for x in (1,2):
                for p in self._order:
                    p = p.deal_to(poker.Deal(deck,1))
            # tell them what cards they got
            for p in self._order:
            irc.reply("Cards dealt.  Let's see some action.")
            return
        if self._state == -1:
            pass



class Holdem(callbacks.Plugin):
    """poker"""
    def __init__(self,irc):
        callbacks.Plugin.__init__(self,irc)

    def board(self,irc,msg,args):
        irc.reply(",".join([ poker.GetCard(c) for c in self._board]))


    def _new_player(self, player):
        self._players.append(player) 
        self._bank[player] = self._starting_cash
        if 1==len(self._players):
            self._dealerBtn = player

    def sit(self,irc,msg,args):
        """ site down and play """
        player = msg.nick
        if player in self._players:
            irc.reply("you're already playing. don't be stupid.")
        else:
            self._new_player(player)
            self._big_blind(player)
            irc.reply("ok, you're in the game.")





Class = Holdem

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=78:
