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
import poker, random, copy

NumOfHands=30
NumPlayers=10
wincount=0

random.seed(7978)
for i in range(0,NumOfHands):
    ThisGame=poker.HoldEmGame(NumPlayers)
    Card1=[1, 3]
    Card2=[1, 2]
    ThisGame.SetHoleCards(0, Card1, Card2)
    for j in range(1,NumPlayers):
        ThisGame.RandomHoleCards(j)
    ThisGame.DealBoard()
    Rank, Hole, Board, HandString=ThisGame.GetWinner()
    ThisGame.DumpStatus()
    if Hole==[Card1, Card2]:
        wincount=wincount+1
        print '(%d/%d) %8.5f Winner: %s' % \
              (wincount, i+1, float(wincount)/float(i+1), HandString)
    else:
        print '(%d/%d) %8.5f Loser: %s' % \
              (wincount, i+1, float(wincount)/float(i+1), HandString)
    
  
