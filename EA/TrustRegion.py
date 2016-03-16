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
# $Id: TrustRegion.py 88 2011-02-19 19:17:27Z kato $

import numpy, copy

class FilterFunctor(object):

	def __init__(self, region):

		self.Lower = region.DesignParameters.MinAsVector()
		self.Upper = region.DesignParameters.MaxAsVector()

	def __call__(self, indi):

		v = indi.DesignParameters.AsVector()
		return numpy.all(self.Lower <= v) and numpy.all(v <= self.Upper)

class TrustRegion(object):

	def __init__(self, chromosome):

		self.Chromosome = chromosome # chromosome defines the initial region (the entire region)
		self.Region = copy.deepcopy(self.Chromosome)

	def Reset(self):

		self.Region = copy.deepcopy(self.Chromosome)

	def Resize(self, extent, center = None):

		oldCenter = self.Region.DesignParameters.AsVector()

		lowerLimit = self.Chromosome.DesignParameters.MinAsVector()
		upperLimit = self.Chromosome.DesignParameters.MaxAsVector()
		if center == None:
			center = self.Chromosome.DesignParameters.AsVector()

		D = 0.5 * (upperLimit - lowerLimit)
		DP = upperLimit - center
		DM = center - lowerLimit

		lower = center - extent * DM
		upper = center + extent * DP

		lower = numpy.maximum(lower, lowerLimit)
		upper = numpy.minimum(upper, upperLimit)

		self.Region.DesignParameters.SetToVector(center)
		for i, p in enumerate(self.Region.DesignParameters):
			p.MinValue = lower[i]
			p.MaxValue = upper[i]

	"""
	def ScaleBy(self, scale, center = None):

		oldCenter = self.Region.DesignParameters.AsVector()
		if center == None:
			center = self.Region.DesignParameters.AsVector()
		dCenter = center - oldCenter

		lower = self.Region.DesignParameters.MinAsVector()
		upper = self.Region.DesignParameters.MaxAsVector()

		lower += dCenter
		upper += dCenter

		lower = center + scale * (lower - center)
		upper = center + scale * (upper - center)
		print "  center/lower/upper = ", center, lower, upper

		lowerLimit = self.Chromosome.DesignParameters.MinAsVector()
		upperLimit = self.Chromosome.DesignParameters.MaxAsVector()

		lower = numpy.maximum(lower, lowerLimit)
		upper = numpy.minimum(upper, upperLimit)

		self.Region.DesignParameters.SetToVector(center)
		for i, p in enumerate(self.Region.DesignParameters):
			p.MinValue = lower[i]
			p.MaxValue = upper[i]
	"""

	def FilterPopulation(self, pop):

		return filter(FilterFunctor(self.Region), pop)

	def __str__(self):

		buf = "Center: " + str(self.Region.DesignParameters.AsVector())
		buf += " Min: " + str(self.Region.DesignParameters.MinAsVector())
		buf += " Max: " + str(self.Region.DesignParameters.MaxAsVector())
		return buf

