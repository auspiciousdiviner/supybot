#!/usr/bin/python
# PyPoker - Python based poker subroutine library for simulations
# Copyright (C) 2004  Jeff Ludwig jeff - at - rockytop.net
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# Contact the author:
#   Jeffery Ludwig
#   7 Buttonbush Ct
#   Elkton, MD 21921
import sys, copy, random


class HoldEmGame:
    HoldemPerms=[[5, 4, 3, 2, 1],
                 [6, 4, 3, 2, 1],
                 [7, 4, 3, 2, 1],
                 [6, 5, 3, 2, 1],
                 [7, 5, 3, 2, 1],
                 [7, 6, 3, 2, 1],
                 [6, 5, 4, 2, 1],
                 [7, 5, 4, 2, 1],
                 [7, 6, 4, 2, 1],
                 [7, 6, 5, 2, 1],
                 [6, 5, 4, 3, 1],
                 [7, 5, 4, 3, 1],
                 [7, 6, 4, 3, 1],
                 [7, 6, 5, 3, 1],
                 [7, 6, 5, 4, 1],
                 [6, 5, 4, 3, 2],
                 [7, 5, 4, 3, 2],
                 [7, 6, 4, 3, 2],
                 [7, 6, 5, 3, 2],
                 [7, 6, 5, 4, 2],
                 [7, 6, 5, 4, 3]]

    def __init__(self, NumPlayers):
        self.NumPlayers=NumPlayers
        self.Deck=ShuffleDeck()
        self.HoleList=[]
        for i in range(0,NumPlayers):
            self.HoleList.append([[-1, -1], [-1, -1]])

    def SetHoleCards(self, HandNumber, Card1, Card2):
        self.HoleList[HandNumber]=[Card1, Card2]
        del self.Deck[self.Deck.index(Card1)]
        del self.Deck[self.Deck.index(Card2)]
        
    def RandomHoleCards(self, HandNumber):
        ThisHole=Deal(self.Deck,2)
        self.HoleList[HandNumber]=ThisHole

    def DealBoard(self):
        self.Board=Deal(self.Deck,5)

    def DealAllRandom(self):
        self.Board=Deal(self.Deck,5)
        for i in range(0, self.NumPlayers):
            ThisHole=Deal(self.Deck,2)
            self.HoleList[i]=ThisHole

    def GetWinner(self):
        BestRank=0
        BestHole=[]
        for Hole in self.HoleList:
            Rank,HandString=self.RankHoldem(Hole, self.Board)
            if Rank>BestRank:
                BestRank=Rank
                del BestHole
                BestHole=copy.deepcopy(Hole)
                BestString=HandString
        return BestRank, BestHole, self.Board, BestString
            
    def DumpStatus(self):
        BestRank=0
        BestHole=[]
        print "Board: ",
        PrintHand(self.Board)
        print "\nPlayers: "
        for Hole in self.HoleList:
            Rank,HandString=self.RankHoldem(Hole, self.Board)
            if Rank>BestRank:
                BestRank=Rank
                del BestHole
                BestHole=copy.deepcopy(Hole)
                BestString=copy.deepcopy(HandString)
            PrintHand(Hole)
            print HandString
        print "*** Winner: ",
        PrintHand(BestHole)
        print BestString
    
    def PrintHoldem(self,PocketCards,Board):
        print "(",
        for thiscard in PocketCards:
            try:
                print CardName[thiscard[0]]+SuitName[thiscard[1]],
            except:
                print "Illegal hand to PrintHand(): "
                print inHand
                sys.exit(1)
        print ") ",
        for thiscard in Board:
            try:
                print CardName[thiscard[0]]+SuitName[thiscard[1]]+' ',
            except:
                print "Illegal hand to PrintHand(): "
                print inHand
                sys.exit(1)

    def RankHoldem(self,PocketCards,Board):
        Rank=0
        TotalCards=copy.deepcopy(PocketCards)
        for j in range(0,5):
            TotalCards.append(Board[j])
        LocalHand=[ [0,0], [0,0], [0,0], [0,0], [0,0]] 
        for i in range(0,21):
            for j in range(0,5):
                LocalHand[j]=TotalCards[self.HoldemPerms[i][j]-1]
            ThisRank=RankHand(LocalHand)
            if ThisRank>Rank:
                BestHand=copy.deepcopy(LocalHand)
                Rank=ThisRank
        Rank,HandString=RankHand(BestHand)
        return Rank, HandString
# Global dictionary for card display
CardName = {1:'A',2:'2',3:'3', 4:'4', 5:'5', 6:'6',7:'7',
            8:'8', 9:'9', 10:'T', 11:'J', 12:'Q', 13:'K', 14:'@'}
SuitName = {1:'h', 2:'d', 3:'s', 4:'c'}
LongName = {1: 'Ace',
            2: 'Two',
            3: 'Three',
            4: 'Four',
            5: 'Five',
            6: 'Six',
            7: 'Seven',
            8: 'Eight',
            9: 'Nine',
            10: 'Ten',
            11: 'Jack',
            12: 'Queen',
            13: 'King',
            14: 'Ace'}
PLongName = {1: 'Aces',
            2: 'Twos',
            3: 'Threes',
            4: 'Fours',
            5: 'Fives',
            6: 'Sixs',
            7: 'Sevens',
            8: 'Eights',
            9: 'Nines',
            10: 'Tens',
            11: 'Jacks',
            12: 'Queens',
            13: 'Kings',
            14: 'Aces'}

def ShuffleDeck():
    InitDeck=[]
    for i in range(1,14):
        for j in range(1,5):
            InitDeck.append([i, j])

    ShuffDeck=[]
    for i in range(0,51):
        z=random.randint(0,51-i)    
        ShuffDeck.append(InitDeck[z])
        del InitDeck[z]

    ShuffDeck.append(InitDeck[0])

    return ShuffDeck

def Deal(Deck, NumCards):
    thisHand=Deck[0:NumCards]
    del Deck[0:NumCards]
    return thisHand

def GetCard(inCard):
    try:
        return "%c%c"%(CardName[inCard[0]],SuitName[inCard[1]])
    except:
        return "Bad card passed to PrintCard()"

def PrintCard(inCard):
    print GetCard(inCard)

def PrintHand(inHand):
    """
    This subroutine takes a 5x2 list as an input and displays
    the hand in a Human readable format such as: Kd, As, etc
    """
    for thiscard in inHand:
        try:
            print CardName[thiscard[0]]+SuitName[thiscard[1]]+' ',
        except:
            print "Illegal hand to PrintHand(): "
            print inHand
            sys.exit(1)

def AcesHigh(inHand):
    """
    Takes a standard hand object as an input and changes the value of
    every ace from 1 to 14.  This is necessary to check for both ace
    high and low straights.
    """
    for thiscard in inHand:
        if thiscard[0]==1:
            thiscard[0]=14            

def AcesLow(inHand):
    """
    Takes a standard hand object as an input and changes the value of
    every ace from 1 to 14.  This is necessary to check for both ace
    high and low straights.
    """
    for thiscard in inHand:
        if thiscard[0]==14:
            thiscard[0]=1            

def RankHand(inHand):
    """
    Returns a numerical ranking (score) for a hand which in principle
    is unique.
    """
    # Initialize score and make copy of passed hand
    Rank=0
    localHand=copy.deepcopy(inHand)

    # First check for straight flush, 9000000+ pts
    StrLow,B,C,D,StrHigh=CheckStraight(localHand)

    # We have a straight flush, rank it
    if (StrLow!=0):
        A,B,C,D,E=CheckFlush(localHand)
        if (A!=0):
            Rank=9000000+10000*StrHigh
            HandString="%s thru %s straight flush (%d)" % \
                  (LongName[StrHigh], LongName[StrLow],Rank)        
            return Rank, HandString
    
    # Check for 4 of a kind, 8MM to 9MM
    FourFlag,FourCard=CheckFourOfAKind(localHand)
    if FourFlag!=0:
        Rank=8000000+FourFlag*10000
        HandString="Four of a kind %s, %s kicker (%d)" % \
              (PLongName[FourCard],LongName[FourFlag], Rank)
        return Rank, HandString

    # Check for Boat, 7MM to 8MM
    AcesHigh(localHand)
    ThreeCard,TwoCard=CheckBoat(localHand)
    if ThreeCard!=0:
        Rank=7000000+ThreeCard*10000+TwoCard*1000
        HandString="Full house, %s over %s (%d)" % \
              (PLongName[ThreeCard], PLongName[TwoCard], Rank)
        return Rank, HandString
    AcesLow(localHand)

    # Check for flush, 6MM to 7MM
    A,B,C,D,E=CheckFlush(localHand)
    if A!=0:
        Rank=6000000+10000*A+1000*B+100*C+10*D+E
        HandString="%s high flush (%d)" % (LongName[A], Rank)
        return Rank, HandString

    # Check for straight, 5MM to 6MM
    StrLow,B,C,D,StrHigh=CheckStraight(localHand)
    if StrLow!=0:
        Rank=5000000+10000*StrHigh
        HandString="Straight, %s thru %s (%d)" % \
              (LongName[StrHigh], LongName[StrLow], Rank)
        return Rank, HandString

    # Check for trips, 4MM to 5MM
    A,B,C=CheckTrips(localHand)
    if A!=0:
        Rank=4000000+10000*A+1000*B+100*C
        HandString="Three of a kind %s, with %s and %s kickers (%d)" % \
              (PLongName[A], LongName[B], LongName[C], Rank)
        return Rank, HandString

    # Check for two pair, 3MM to 4MM
    A,B,C=CheckTwoPair(localHand)
    if A!=0:
        Rank=3000000+A*10000+B*1000+C*100
        HandString="Two Pair, %s and %s, %s kicker (%d)" % \
              (PLongName[A], PLongName[B], LongName[C], Rank)
        return Rank, HandString

    # Check for pairs, 2MM to 3MM
    A,B,C,D=CheckPair(localHand)
    if A!=0:
        Rank=2000000+10000*A+1000*B+100*C+10*D
        HandString="Pair of %s, %s, %s, %s as kickers (%d)" % \
              (PLongName[A], LongName[B], LongName[C], LongName[D], Rank)
        return Rank, HandString

    A,B,C,D,E=HighCard(localHand)
    Rank=10000*A+1000*B+100*C+10*D+E
    HandString="%s high (%d)" % (LongName[A], Rank)
    return Rank, HandString

def HighCard(inHand):
    AcesHigh(inHand)
    inHand.sort()
    inHand.reverse()

    return inHand[0][0],inHand[1][0],inHand[2][0],inHand[3][0],inHand[4][0]

def CheckTwoPair(inHand):
    AcesHigh(inHand)
    inHand.sort()
    inHand.reverse()

    # AA BB C
    if (inHand[0][0]==inHand[1][0]) & (inHand[2][0]==inHand[3][0]):
        return inHand[0][0], inHand[2][0], inHand[4][0] 

    # AA B CC
    if (inHand[0][0]==inHand[1][0]) & (inHand[3][0]==inHand[4][0]):
        return inHand[0][0], inHand[4][0], inHand[2][0]

    # A BB CC
    if (inHand[1][0]==inHand[2][0]) & (inHand[3][0]==inHand[4][0]):
        return inHand[1][0], inHand[3][0], inHand[0][0] 

    return 0, 0, 0


def CheckPair(inHand):
    AcesHigh(inHand)
    inHand.sort()
    inHand.reverse()

    # AA B C D
    if (inHand[0][0]==inHand[1][0]):
        return inHand[0][0], inHand[2][0], inHand[3][0], inHand[4][0] 

    # A BB C D
    if (inHand[1][0]==inHand[2][0]):
        return inHand[1][0], inHand[0][0], inHand[3][0], inHand[4][0] 

    # A BB C D
    if (inHand[2][0]==inHand[3][0]):
        return inHand[2][0], inHand[0][0], inHand[1][0], inHand[4][0] 

    # A BB C D
    if (inHand[3][0]==inHand[4][0]):
        return inHand[3][0], inHand[0][0], inHand[1][0], inHand[2][0] 

    return 0, 0, 0, 0


def CheckTrips(inHand):
    AcesHigh(inHand)
    inHand.sort()
    inHand.reverse()
    FoundTrips=0
    TripLoc=0
    for i in range(0,3):
        thiscard=inHand[i][0]
        if (inHand[i+1][0]==thiscard) & (inHand[i+2][0]==thiscard):
            TripCard=thiscard
            FoundTrips=1
            TripLoc=i

    if FoundTrips==0:
        return 0, 0, 0

    if TripLoc==0:
        Kicker1=inHand[3][0]
        Kicker2=inHand[4][0]

    if TripLoc==1:
        Kicker1=inHand[0][0]
        Kicker2=inHand[4][0]

    if TripLoc==2:
        Kicker1=inHand[0][0]
        Kicker2=inHand[1][0]


    return TripCard, Kicker1, Kicker2

def CheckBoat(inHand):
    """
    Checks for a full house returns 3 card and 2 card if present, 0 if not
    """
    BoatFlag=1
    inHand.sort()
    ThreeCard=inHand[0][0]
    for i in range(1,3):
        if ThreeCard!=inHand[i][0]:
            BoatFlag=0
    TwoCard=inHand[3][0]
    if TwoCard!=inHand[4][0]:
        BoatFlag=0

    if BoatFlag==1:
        return ThreeCard, TwoCard

    # Now check the other way
    BoatFlag=1
    inHand.reverse()
    ThreeCard=inHand[0][0]
    for i in range(1,3):
        if ThreeCard!=inHand[i][0]:
            BoatFlag=0
    TwoCard=inHand[3][0]
    if TwoCard!=inHand[4][0]:
        BoatFlag=0

    if BoatFlag==1:
        return ThreeCard, TwoCard

    return 0, 0

def CheckFourOfAKind(inHand):
    """ Returns 0 if doesn't exit, else returns kicker """
    FourFlag=1
    AcesHigh(inHand)
    inHand.sort()

    # Check low to high first
    firstcard=inHand[0][0]
    for i in range(1,4):
        if inHand[i][0]!=firstcard:
            FourFlag=0

    if FourFlag==1:
        # Return kicker card
        return inHand[4][0], inHand[0][0]

    # Check high to low
    FourFlag=1
    inHand.reverse()
    firstcard=inHand[0][0]
    for i in range(1,4):
        if inHand[i][0]!=firstcard:
            FourFlag=0

    if FourFlag==1:
        # Return kicker card
        return inHand[4][0], inHand[0][0]

    return FourFlag, inHand[0][0]

def CheckFlush(inHand):
    """
    Check inHand for flush
    """
    AcesHigh(inHand)
    inHand.sort()
    inHand.reverse()
    suit=inHand[0][1]
    FoundFlush=1
    for i in range(1,5):
        if suit!=inHand[i][1]:
            FoundFlush=0

    if FoundFlush==1:
        return inHand[0][0],inHand[1][0],inHand[2][0],inHand[3][0],inHand[4][0]
    else:
        return 0, 0, 0, 0, 0

def CheckStraight(inHand):
    """
    Checks to see if passed hand is a straight, high or low Ace.
    """
    AcesLow(inHand)
    FoundStraight=1
    inHand.sort()
    check=inHand[0][0]
    for card in inHand:
        if card[0]!=check:
            FoundStraight=0
        check=check+1

    # If we found it return
    if FoundStraight==1:
        return inHand[0][0],inHand[1][0],inHand[2][0],inHand[3][0],inHand[4][0]

    FoundStraight=1
    AcesHigh(inHand)
    inHand.sort()

    check=inHand[0][0]
    for card in inHand:
        if card[0]!=check:
            FoundStraight=0
        check=check+1

    # If we found it return
    if FoundStraight==1:
        return inHand[0][0],inHand[1][0],inHand[2][0],inHand[3][0],inHand[4][0]

    # Return hand
    AcesLow(inHand)

    return 0,0,0,0,0
