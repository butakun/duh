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
# $Id: InfillSandbox.py 130 2013-10-29 01:15:50Z kato $

import numpy as np
import random

def LHS(numParams, numSamples):

	X = np.zeros((numSamples, numParams))
	for d in range(numParams):
		p = np.linspace(0.0, 1.0, numSamples)
		random.shuffle(p)
		X[:, d] = p
	return X

class InfillSandbox(list):

	def __init__(self, chain):
		xmin, xmax, xref = chain.ParameterSpecsAsVectors()
		self.XMin, self.XMax = xmin, xmax
		self.LHSNumSamples = 1000

	def AddSite(self, x, f):

		self.append([np.array(x), f])

	def ComputeNormalizedSites(self):

		numSites = len(self)
		numParams = len(self.XMin)
		dx = self.XMax - self.XMin
		normalized = []
		for s in self:
			x, f = s
			xnormalized = (x - self.XMin) / dx
			normalized.append([xnormalized, f])
		return normalized

	def FindNewSites(self, numNewSites):

		normalizedSites = self.ComputeNormalizedSites()

		numParams = len(self.XMin)
		candidateSites = LHS(numParams, self.LHSNumSamples)

		# Gather parametric positions of existing sites
		X = np.zeros((len(self), numParams))
		for i in range(len(self)):
			X[i, :] = normalizedSites[i][0]
		print "X = "
		print X

		infillPotential = np.zeros(len(candidateSites))
		infillNearest = []
		for i in range(len(candidateSites)):
			x = candidateSites[i, :]
			dx = X - x
			dx = dx * dx
			dx = dx.sum(axis = 1)
			j = dx.argmin() # the existing sample closest to x
			dxmin = dx[j]
			metric = normalizedSites[j][1]
			infillPotential[i] = dxmin * metric
			infillNearest.append(j)

		indices = infillPotential.argsort()
		newSites = []
		dx = self.XMax - self.XMin
		for i in indices[-1:-1-numNewSites:-1]:
			xnormalized = candidateSites[i, :]
			x = xnormalized * dx + self.XMin
			newSites.append([x, infillPotential[i], infillNearest[i]])

		return newSites

