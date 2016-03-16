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
# $Id$

import EA

class Optimizer(object):

	def __init__(self, spec, chromosome, resEval):

		self.Chromosome = chromosome
		self.ResEval = resEval

	def Start(self):

		pop = EA.Population()
		for i in range(5):
			indi = self.Chromosome.Clone()
			pop.append(indi)
		print pop

		self.ResEval.Evaluate(pop)

