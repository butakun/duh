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
# $Id: LineRecombinationOperator.py 12 2010-04-09 15:12:40Z kato $

from RecombinationOperator import RecombinationOperator
import numpy as n

class LineRecombinationOperator(RecombinationOperator):

	def __init__(self, e1):
		"""
		Given two parents
		"""

		assert(e1 > 0.0)
		self.e1 = e1

	def Combine(self, individuals):

		assert(len(individuals) == 2)
		v1 = individuals[0].DesignParameters.AsVector()
		v2 = individuals[1].DesignParameters.AsVector()
		r = n.random.random()
		a = (1.0 - r) * (-self.e1) + r * (1.0 + self.e1)
		v = (1.0 - a) * v1 + a * v2

		offspring = individuals[0].Clone()
		offspring.Initialize()
		offspring.DesignParameters.SetToVector(v)
		return offspring

