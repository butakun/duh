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
# $Id: TournamentSelectionOperator.py 12 2010-04-09 15:12:40Z kato $

from SelectionOperator import SelectionOperator
import numpy as n

class TournamentSelectionOperator(SelectionOperator):

	def __init__(self, tours, nSelect):
		"""
		Using tournament of "tours" individuals, and selects "nSelect" individuals.
		"""

		self.Tours = tours
		self.NSelect = nSelect

	def Select(self, population):

		iselected = []
		while len(iselected) < self.NSelect:
			picked = n.random.random_integers(0, len(population) - 1, self.Tours)
			iwinner = picked[0]
			for i in picked[1:]:
				if population[i].Fitness > population[iwinner].Fitness:
					iwinner = i
			if not iwinner in iselected:
				iselected.append(iwinner)

		selected = []
		for i in iselected:
			selected.append(population[i])
		return selected

