###
# Copyright (c) 2012, resistivecorpse
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.conf as conf
import random as random
import re
import time
import string
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('HuntNFish')

try:
    with open(conf.supybot.directories.data.dirize('hunttrophy.txt')) as f: pass
except IOError:
    with open(conf.supybot.directories.data.dirize('hunttrophy.txt'), 'w') as file:
        file.writelines('Nobody\n nothing\n2')

try:
    with open(conf.supybot.directories.data.dirize('fishtrophy.txt')) as f: pass
except IOError:
    with open(conf.supybot.directories.data.dirize('fishtrophy.txt'), 'w') as file:
        file.writelines('Nobody\n nothing\n2')

@internationalizeDocstring
class HuntNFish(callbacks.Plugin):
    """Adds hunt and fish commands for a basic hunting and fishing game."""

    threaded = True

    def __init__(self, irc):
        self.__parent = super(HuntNFish, self)
        self.__parent.__init__(irc)
        self._huntersEndTime = {}
        self._fishersEndTime = {}
        
        
    def hunt(self,irc,msg,args, channel):
        """
        performs a random hunt
        """

        channel = ircutils.toLower(channel)
        timeoutLength = self.registryValue('timeout')
        player = msg.prefix
        currentTime = time.time()

        if player in self._huntersEndTime and self._huntersEndTime[player] > currentTime:
            irc.reply("Hold on, your weapon is reloading... {0}".format(
                      time.strftime("%M minute(s) and %S more second(s) left until we're ready!", self._huntersEndTime[player] - currentTime)))
        else:
            endTime = currentTime + timeoutLength
            self._huntersEndTime[player] = endTime
            if(self.registryValue('enable', msg.args[0])):
                
                animals = ['bear', 'gopher', 'rabbit', 'hunter', 'deer', 'fox', 'duck', 
                           'moose', 'pokemon named Pikachu', 'park ranger', 'Yogi Bear', 
                           'Boo Boo Bear', 'dog named Benji', 'cow', 'raccoon', 'koala bear', 
                           'camper', 'channel lamer', 'your mom', 'dog', 'cat', 'bird', 'turkey'
                           'chicken', 'monkey', 'gorilla', 'bat', 'construction worker',
                           'World of Warcraft nerd', 'nerd', 'moving car', 'possum', 'kangaroo', 'rat',
                           'cockroach', 'radroach', 'tiger', 'lion', 'puma', 'panther', 'mountain lion',
                           'wolf', 'caribou', 'reindeer', 'polar bear', 'man', 'woman', 'komodo dragon',
                           'alligator', 'crocidile', 'beached whale', 'parked car', 'tree', 'trash can',
                           'soda can', 'lynx', 'coyote', 'dingo', 'feral dog', 'feral cat', 'white tiger',
                           'tapir', 'parrot', 'hawk', 'eagle', 'bald eagle', 'falcon', 'pig', 'boar', 'brahmin',
                           'yao guai', 'deathclaw', 'golden gecko', 'hydra', 'snake', 'house', 'skyscraper',
                           'draugr', 'sheep', 'goat', ]

                places = ['in some bushes', 'in a hunting blind', 'in a hole', 'up in a tree', 
                          'in a hiding place', 'out in the open', 'in the middle of a field',
                          'downtown', 'on a street corner', 'at the local mall', 'in a residential neighborhood',
                          'uptown', 'midtown', 'in a Brazilian rainforest', 'in an African rainforest', 
                          'in {0}\'s house'.format(player), 'in a house', 'in the Sahara desert', 'in the Gobi desert',
                          'in the Mojave desert', 'in a landfill', 'at an airport', 'in a school', 'at the edge of the universe',
                          'in a jungle', 'in a Wal-mart', 'in a parking lot', 'in the forest', 'at point-blank range']

                with open(conf.supybot.directories.data.dirize('hunttrophy.txt'), 'r') as file:
                    data = file.readlines()
                    highScore = data[2].rstrip('\n')
                huntrandom = random.getstate()   
                random.seed(time.time())
                currentWhat = random.choice(animals)
                currentWhere = random.choice(places)
                weight = random.randint(int(highScore)/2,int(highScore)+13)
                weightType = self.registryValue('weightType')
                irc.reply("{0} goes hunting {1} for a {2}{3} {4}...".format(msg.nick, currentWhere, weight, weightType,
                                                                            currentWhat))
                irc.reply("Aims....")
                irc.reply("Fires.....")
                time.sleep(random.randint(4,8))#pauses the output between line 1 and 2 for 4-8 seconds
                huntChance = random.randint(1,100)
                successRate = self.registryValue('SuccessRate')
                random.setstate(huntrandom)

                if huntChance < successRate:

                    irc.reply("Way to go, {0}. You killed the {1}{2} {3}!".format( msg.nick, weight, weightType,
                                                                                   currentWhat))
                    with open(conf.supybot.directories.data.dirize('hunttrophy.txt'), 'r') as file:
                        data = file.readlines()
                        bigHunt = data[2].rstrip('\n')
                        if weight > int(bigHunt):
                            with open(conf.supybot.directories.data.dirize('hunttrophy.txt'), 'w') as file:
                                data[0] = msg.nick
                                data[1] = currentWhat 
                                data[2] = weight
                                file.writelines(str(data[0]))
                                file.writelines('\n')
                                file.writelines(str(data[1]))
                                file.writelines('\n')
                                file.writelines(str(data[2]))
                                irc.reply("You got a new highscore!")


                else:
                    irc.reply("Oops, you missed, {0}. You should get some glasses to fix that eyesight of yours".format(msg.nick))
    hunt = wrap(hunt, ['Channel'])
    
    def fish(self,irc,msg,args, channel):
        """
        performs a random fishing trip
        """

        channel = ircutils.toLower(channel)
        timeoutLength = self.registryValue('timeout')
        player = msg.prefix
        currentTime = time.time()

        if player in self._fishersEndTime and self._fishersEndTime[player] > currentTime:
            irc.reply("Hold on, still putting bait on your fishing pole... {0}".format(
                      time.strftime("%M minute(s) and %S more second(s) left until we're ready!", self._fishersEndTime[player] - currentTime)))
        else:
            endTime = currentTime + timeoutLength
            self._fishersEndTime[player] = endTime
            if(self.registryValue('enable', msg.args[0])):
                fishes = ('Salmon', 'Herring', 'Yellowfin Tuna', 'Pink Salmon', 'Chub', 'Barbel', 'Perch', 
                          'Northern Pike', 'Brown Trout', 'Arctic Char', 'Roach', 'Brayling', 'Bleak', 
                          'Cat Fish', 'Sun Fish', 'Old Tire', 'Rusty Tin Can', 'Genie Lamp', 
                          'Love Message In A Bottle', 'Old Log', 'Rubber Boot' , ' Dead Body', ' Loch Ness Monster',
                          'Old Fishing Lure', 'Piece of the Titanic', 'Chunk of Atlantis', 'Squid', 'Whale', 
                          'Dolphin',  'Porpoise' , 'Stingray', 'Submarine', 'Seal', 'Seahorse', 'Jellyfish', 
                          'Starfish', 'Electric Eel', 'Great White Shark', 'Scuba Diver' , 'Lag Monster', 
                          'Virus', 'Soggy Pack of Smokes', 'Bag of Weed', 'Boat Anchor', 'Pair Of Floaties', 
                          'Mermaid', 'Merman', 'Halibut', 'Tiddler', 'Sock', 'Trout', 'Blinky the Fish', 'Chthulu',
                          'Magikarp', 'Seaking', 'Narwhal', 'Orca whale', 'Old Gym Sock', 'Octopus', 'Kraken',
                          'Plastic Bag of Water', 'Eel', 'Rusty Pipe', 'Dog Collar', 'Pair of Pants')
                          
                fishSpots = ('a Stream', 'a Lake', 'a River', 'a Pond', 'an Ocean', 'a Bathtub', 
                             'a Kiddies Swimming Pool', 'a Toilet', 'a Pile of Vomit', 'a Pool of Urine', 
                             'a Kitchen Sink', 'a Bathroom Sink', 'a Mud Puddle', 'a Pail of Water', 'a Bowl of Jell-O', 
                             'a Wash Basin', 'a Rain Barrel', 'an Aquarium', 'a SnowBank', 'a WaterFall', 
                             'a Cup of Coffee', 'a Glass of Milk', 'a Glass of Water', 'a Puddle', 'a Raindrop',
                             'a Portapotty', 'a Fountain', 'a Blood Puddle')

                with open(conf.supybot.directories.data.dirize('fishtrophy.txt'), 'r') as file:
                    data = file.readlines()
                    highScore = data[2].rstrip('\n')
                fishrandom = random.getstate()
                random.seed(time.time())
                currentWhat = random.choice(fishes)
                currentWhere = random.choice(fishSpots)
                weight = random.randint(int(highScore)/2,int(highScore)+13)
                weightType = self.registryValue('weightType')
                irc.reply("{0} goes fishing in {1}.".format(msg.nick, currentWhere))
                irc.reply("Casts a line in....")
                irc.reply("A {0}{1} {2} is biting....".format(weight, weightType, currentWhat))
                time.sleep(random.randint(4,8))#pauses the output between line 1 and 2 for 4-8 seconds
                huntChance = random.randint(1,100)
                successRate = self.registryValue('SuccessRate')
                random.setstate(fishrandom)

                if huntChance < successRate:
                    irc.reply("Way to go, {0}. You caught the {1}{2} {3}!".format(msg.nick, weight, weightType, currentWhat))
                    with open(conf.supybot.directories.data.dirize('fishtrophy.txt'), 'r') as file:
                        data = file.readlines()
                        bigFish = data[2].rstrip('\n')
                        if weight > int(bigFish):
                            with open(conf.supybot.directories.data.dirize('fishtrophy.txt'), 'w') as file:
                                data[0] = msg.nick
                                data[1] = currentWhat 
                                data[2] = weight
                                file.writelines(str(data[0]))
                                file.writelines('\n')
                                file.writelines(str(data[1]))
                                file.writelines('\n')
                                file.writelines(str(data[2]))
                                irc.reply("You got a new highscore!")


                else:
                    irc.reply("Oops, it got away, {0}. Don't quit your day job to become a fisher...".format(msg.nick))
    fish = wrap(fish, ['Channel'])

    def trophy(self,irc,msg,args):
        """
        checks the current highscores for hunting and fishing
        """
        if(self.registryValue('enable', msg.args[0])):
            weightType = self.registryValue('weightType')
            with open(conf.supybot.directories.data.dirize('hunttrophy.txt'), 'r') as file1:
                data1 = file1.readlines()
                hunter = data1[0].rstrip('\n')
                hunted = data1[1].rstrip('\n')
                score = data1[2].rstrip('\n')
                irc.reply("The hunting highscore held by: {0} with a {1}{2} {3}.".format(hunter, score, weightType, hunted))
            with open(conf.supybot.directories.data.dirize('fishtrophy.txt'), 'r') as file2:
                data2 = file2.readlines()
                fisherman = data2[0].rstrip('\n')
                catch = data2[1].rstrip('\n')
                size = data2[2].rstrip('\n')
                irc.reply("The fishing highscore held by: {0} with a {1}{2} {3}.".format(fisherman, size, weightType, catch))



Class = HuntNFish


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
