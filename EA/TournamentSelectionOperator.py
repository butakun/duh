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

