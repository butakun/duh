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

