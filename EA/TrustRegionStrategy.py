# $Id: TrustRegionStrategy.py 69 2010-12-28 07:06:59Z kato $

from TrustRegion import TrustRegion
from Population import Population

class TrustRegionStrategy(object):

	def __init__(self, scalingWhenImproved, scalingWhenNotImproved):

		self.ScalingWhenImproved = scalingWhenImproved
		self.ScalingWhenNotImproved = scalingWhenNotImproved
		self.Scale = 1.0

	def AdaptTrustRegion(self, trust, population, bestCandidate, bestSoFar, fitnessEval):

		tmp = Population()
		tmp.append(bestCandidate)
		tmp.append(bestSoFar)
		finessEval.Evaluate(tmp)

		improved = bestCandidate.Fitness > bestSoFat.Fitness

		if improved:
			print "Improved"
			self.Scale *= self.ScalingWhenImproved
		else:
			print "Did not improve"
			self.Scale *= self.ScalingWhenNotImproved

		self.Scale = min(self.Scale, 1.0)

		center = bestCandidate.DesignParameters.AsVector()

		trust.Reset()
		trust.ScaleBy(self.Scale, center)

		numParams = len(bestCandidate.DesignParameters)
		numSuccessfuls = len(population.SuccessfulIndividuals())


		print "Trust Region: ", trust

