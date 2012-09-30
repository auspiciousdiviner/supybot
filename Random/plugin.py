import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
import random

_ = PluginInternationalization('Random')

@internationalizeDocstring
class Random(callbacks.Plugin):
    """This plugin provides a few random number commands and some
        commands for getting random samples.  Use the "seed" command to seed
        the plugin's random number generator if you like, though it is
        unnecessary as it gets seeded upon loading of the plugin. The
        "random" command is most likely what you're looking for, though
        there are a number of other useful commands in this plugin.  Use
        'list Random' to check them out."""
    threaded = True

    def __init__(self, irc):
        self.__parent = super(Random, self)
        self.__parent.__init__(irc)
        self.rng = random.Random()   # create our rng
        self.rng.seed()   # automatically seeds with current time

    def binary(self, irc, msg, args, length):
        """<binary_length>

        Generates a binary number that's <length> long.
        """
        numberSet = [ 

                         '0', '1'

                       ]

        stringToAddTo = ''

        if length < 0:
            irc.reply("Error: Length is too small.")
        else:
            for length in range(0, length):
                stringToAddTo += random.choice(numberSet)
            irc.reply(stringToAddTo)

    binary = wrap(binary, ['int'])

    def card(self, irc, msg, args):
        """takes no arguments

        Returns a random card from a deck of 52 cards.
        """

        deck = [  
                  "Ace of Spades", "2 of Spades", "3 of Spades", "4 of Spades", 
                  "5 of Spades", "6 of Spades", "7 of Spades", "8 of Spades", "9 of Spades", 
                  "10 of Spades", "Jack of Spades", "Queen of Spades", "King of Spades", 

                  "Ace of Hearts", "2 of Hearts", "3 of Hearts", "4 of Hearts", 
                  "5 of Hearts", "6 of Hearts", "7 of Hearts", "8 of Hearts", "9 of Hearts", 
                  "10 of Hearts", "Jack of Hearts", "Queen of Hearts", "King of Hearts", 

                  "Ace of Diamonds", "2 of Diamonds", "3 of Diamonds", "4 of Diamonds", 
                  "5 of Diamonds", "6 of Diamonds", "7 of Diamonds", "8 of Diamonds", "9 of Diamonds", 
                  "10 of Diamonds", "Jack of Diamonds", "Queen of Diamonds", "King of Diamonds", 

                  "Ace of Clubs", "2 of Clubs", "3 of Clubs", "4 of Clubs", 
                  "5 of Clubs", "6 of Clubs", "7 of Clubs", "8 of Clubs", "9 of Clubs", 
                  "10 of Clubs", "Jack of Clubs", "Queen of Clubs", "King of Clubs"
               ]

        irc.reply('%s' % ''.join(map(str, random.choice(deck))))
    card = wrap(card)

    def cards(self, irc, msg, args, cards_to_sample):
        """<cards_to_sample> (can be no greater than 52) or less than 1

        Returns a <cards_to_sample> large sample of cards from a 52 card deck
        """

        deck = [  
                  "Ace of Spades", "2 of Spades", "3 of Spades", "4 of Spades", 
                  "5 of Spades", "6 of Spades", "7 of Spades", "8 of Spades", "9 of Spades", 
                  "10 of Spades", "Jack of Spades", "Queen of Spades", "King of Spades", 

                  "Ace of Hearts", "2 of Hearts", "3 of Hearts", "4 of Hearts", 
                  "5 of Hearts", "6 of Hearts", "7 of Hearts", "8 of Hearts", "9 of Hearts", 
                  "10 of Hearts", "Jack of Hearts", "Queen of Hearts", "King of Hearts", 

                  "Ace of Diamonds", "2 of Diamonds", "3 of Diamonds", "4 of Diamonds", 
                  "5 of Diamonds", "6 of Diamonds", "7 of Diamonds", "8 of Diamonds", "9 of Diamonds", 
                  "10 of Diamonds", "Jack of Diamonds", "Queen of Diamonds", "King of Diamonds", 

                  "Ace of Clubs", "2 of Clubs", "3 of Clubs", "4 of Clubs", 
                  "5 of Clubs", "6 of Clubs", "7 of Clubs", "8 of Clubs", "9 of Clubs", 
                  "10 of Clubs", "Jack of Clubs", "Queen of Clubs", "King of Clubs"
            ]

        if cards_to_sample > 52:
            irc.reply("Error: Input too big.")
        elif cards_to_sample < 1:
            irc.reply("Error: Input too small.")
        else:
            irc.reply('%s' % ', '.join(map(str, random.sample(deck, cards_to_sample))))
    cards = wrap(cards, ['int'])

    def coins(self, irc, msg, args, coins):
        """<coins> 

        Returns a survey of <coins> flipped, showing both the amount of heads and tails.
        """

        coin = [ 0, 1 ] # 0 = Heads, 1 = tails

        heads = 0
        tails = 0

        if coins < 0:
            irc.reply("Error: Coin value too small.")
        elif coins > self.registryValue('maxCoins'):
            irc.reply("Error: This number of coins exceeds the set limit.")
        else:
            for coins in range(0, coins):
                if random.choice(coin) == 0:
                    heads += 1
                else:
                    tails += 1
            irc.reply("Heads: %s Tails: %s" % (heads, tails))
    coins = wrap(coins, ['int'])

    def hex(self, irc, msg, args, length):
        """<hex_length>

        Generates a hexadecimal number that's <length> long.
        """
        hexSet = [ 

                         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',

                       ]

        stringToAddTo = ''

        if length < 0:
            irc.reply("Error: Length is too small.")
        else:
            for length in range(0, length):
                stringToAddTo += random.choice(hexSet)
            irc.reply(stringToAddTo)

    hex = wrap(hex, ['int'])

    def random(self, irc, msg, args):
        """takes no arguments

        Returns the next random number from the random number generator.
        """
        irc.reply(str(random.random()))
    random = wrap(random)

    def range(self, irc, msg, args, n1, n2):
        """<min_value> <max_value>

        Returns a random whole number in the range of <max_value> and <min_value>.
        """

        s = self.rng.randrange(n1, n2)
        irc.reply(s)
    range = wrap(range, ['int', 'int'])

    def seed(self, irc, msg, args, seed):
        """<seed>

        Sets the internal RNG's seed value to <seed>.  <seed> must be a
        floating point number.
        """
        self.rng.seed(seed)
        irc.replySuccess()
    seed = wrap(seed, ['float'])

    def string(self, irc, msg, args, length):
        """<character_length>

        Makes a string that's <length> characters long; spaces are included also.
        """
        characterSet = [ 

                         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                         ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_',
                         '=', '+', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{',
                         '[', '}', ']', '\\', '|', ';', ':', '\"', '\'', ',', '<', '>', '.',
                         '/', '?',

                       ]

        stringToAddTo = ''

        if length < 0:
            irc.reply("Error: Length is too small.")
        else:
            for length in range(0, length):
                stringToAddTo += random.choice(characterSet)
            irc.reply(stringToAddTo)

    string = wrap(string, ['int'])

    def text(self, irc, msg, args, length):
        """<character_length>

        Makes a string that's <length> alphanumeric numbers long.
        """
        characterSet = [ 

                         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                         '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',

                       ]

        stringToAddTo = ''

        if length < 0:
            irc.reply("Error: Length is too small.")
        else:
            for length in range(0, length):
                stringToAddTo += random.choice(characterSet)
            irc.reply(stringToAddTo)

    text = wrap(text, ['int'])

Class = Random

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
