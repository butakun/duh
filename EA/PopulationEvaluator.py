# $Id: PopulationEvaluator.py 2 2010-02-26 14:01:03Z kato $

class PopulationEvaluator(object):

	def Evaluate(self, indipop):

		if issubclass(type(indipop), list):
			for indi in indipop:
				self.Function(indi)
		else:
			self.Function(indipop)

