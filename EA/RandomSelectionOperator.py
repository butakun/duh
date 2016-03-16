# $Id: RandomSelectionOperator.py 2 2010-02-26 14:01:03Z kato $

from SelectionOperator import SelectionOperator
import random

class RandomSelectionOperator(SelectionOperator):

	def __init__(self, numOffsprings = 2):

		self.NumOffsprings = numOffsprings

	def Select(self, parents):

		return random.sample(parents, self.NumOffsprings)

