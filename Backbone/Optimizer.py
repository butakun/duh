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

