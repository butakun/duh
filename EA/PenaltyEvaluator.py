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
# $Id: PenaltyEvaluator.py 2 2010-02-26 14:01:03Z kato $

from PopulationEvaluator import PopulationEvaluator
from Penalty import Penalty
import numpy as n

class PenaltyEvaluator(PopulationEvaluator):

	def __init__(self):

		self.ObjectivePenalties = []
		self.ConstraintPenalties = []

	def Function(self, indi):

		o, c = [], []
		for penalty in self.ObjectivePenalties:
			o.append(penalty.Apply(indi))
		for penalty in self.ConstraintPenalties:
			c.append(penalty.Apply(indi))
		o = n.array(o)
		c = n.array(c)

		indi.Objectives = o
		indi.Constraints = c

