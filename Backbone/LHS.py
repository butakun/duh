#    duh, a heuristics-based design exploration code.
#    Copyright (C) 2016 Hiromasa Kato <hiromasa at gmail.com>
#
#    This file is part of duh.
#
#    duh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    duh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# $Id: LHS.py 127 2013-05-17 16:35:24Z kato $

import numpy as n
import random

def LHS(sampleCount, dimension):

	pp = n.zeros((sampleCount, dimension))
	for d in range(dimension):
		p = n.linspace(0.0, 1.0, sampleCount)
		random.shuffle(p)
		#for i in range(sampleCount, 1, -1):
		#	j = random.randrange(i)
		#	p[j], p[i - 1] = p[i - 1], p[j]
		pp[:, d] = p
	return pp

