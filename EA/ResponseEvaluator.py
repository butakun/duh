# $Id: ResponseEvaluator.py 2 2010-02-26 14:01:03Z kato $

from PopulationEvaluator import PopulationEvaluator

class ResponseEvaluator(PopulationEvaluator):

	def __init__(self, func):

		self.Functor = func

	def Function(self, indi):

		self.Functor(indi)

