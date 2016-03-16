# $Id: SurrogateResponseEvaluator.py 83 2011-02-03 16:05:19Z kato $

from PopulationEvaluator import PopulationEvaluator

class SurrogateResponseEvaluator(PopulationEvaluator):

	def __init__(self, responseModel, successModel, chromosome):

		self.ResponseSurrogate = responseModel
		self.SuccessSurrogate = successModel
		self.Chromosome = chromosome

	def Function(self, indi):

		x = indi.DesignParameters.AsVector()
		y = self.ResponseSurrogate.Evaluate(x)
		s = self.SuccessSurrogate.Evaluate(x)

		for i, v in enumerate(y):
			indi.Responses[i].Value = v

		indi.Success = s > 0.5

