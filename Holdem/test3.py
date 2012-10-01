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

random.seed(123456)
for i in range(0,100):
    Deck=poker.ShuffleDeck()
    Board=poker.Deal(Deck,5)
    Hole=poker.Deal(Deck,2)
    poker.PrintHoldem(Hole,Board)
    Rank, HandString=poker.RankHoldem(Hole,Board)
    print HandString
    del Hole
    del Board
