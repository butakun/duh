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
# $Id: DrunkRecombinationOperator.py 86 2011-02-17 16:46:06Z kato $

from RecombinationOperator import RecombinationOperator
from LineRecombinationOperator import LineRecombinationOperator
from BoxRecombinationOperator import BoxRecombinationOperator
import numpy as n

class DrunkRecombinationOperator(RecombinationOperator):

	def __init__(self):

		RecombinationOperator.__init__(self)
		ops = []
		ops.append(LineRecombinationOperator(0.25))
		ops.append(BoxRecombinationOperator(0.25))
		self.Operators = ops
		self.Wheel = [0.5, 1.0]

	def Combine(self, individuals):

		r = n.random.random()
		for i, op in enumerate(self.Operators):
			if r <= self.Wheel[i]:
				return op.Combine(individuals)
		raise ValueError
