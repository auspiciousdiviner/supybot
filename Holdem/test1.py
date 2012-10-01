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
import poker, random

# Straight flushs, A high and low
Hands=[]
Hands.append([ [1, 1], [5, 1], [4, 1], [2, 1], [3, 1] ])
Hands.append([ [1, 3], [10, 3], [12, 3], [13, 3], [11, 3] ])

# Four of a kind, kicker higher and lower
Hands.append([ [1, 1], [10, 1], [10, 2], [10, 3], [10, 4] ])
Hands.append([ [3, 1], [5, 1], [5, 2], [5, 3], [5, 4] ])

# Full house high cards as part of high pair / low pair
Hands.append([ [1, 2], [1, 3], [4, 2], [1, 1], [4, 4] ])
Hands.append([ [4, 2], [1, 3], [4, 2], [1, 1], [4, 4] ])

# Flushes
Hands.append([ [4, 2], [9, 2], [11, 2], [3, 2], [1, 2] ])
Hands.append([ [7, 4], [9, 4], [11, 4], [8, 4], [1, 4] ])

# Straights
Hands.append([ [1, 1], [5, 2], [4, 3], [2, 2], [3, 1] ])
Hands.append([ [1, 4], [10, 3], [12, 4], [13, 2], [11, 1] ])

# Trips
Hands.append([ [1, 4], [10, 3], [10, 4], [13, 2], [10, 1] ])
Hands.append([ [5, 4], [10, 3], [10, 4], [13, 2], [10, 1] ])
Hands.append([ [3, 4], [10, 3], [4, 4], [10, 2], [10, 1] ])

# Two Pair
Hands.append([ [1,2], [13,1], [5,2], [13,4], [1,3] ])
Hands.append([ [1,2], [13,1], [5,2], [5,4], [1,3] ])
Hands.append([ [1,2], [13,1], [5,2], [13,4], [5,3] ])

# Pairs
Hands.append([ [6,3], [1,2], [5,2], [1,1], [13,4] ])
Hands.append([ [1,3], [13,2], [3,2], [2,1], [13,4] ])
Hands.append([ [13,3], [1,2], [5,2], [3,1], [5,4] ])
Hands.append([ [3,1], [10,2], [5,2], [6, 3], [3,4] ])

# High cards
Hands.append([ [3,1], [10,2], [5,2], [6, 3], [2,4] ])

for Hand in Hands:
    Rank,HandString=poker.RankHand(Hand)
    poker.PrintHand(Hand)
    print HandString
