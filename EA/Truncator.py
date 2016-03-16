# $Id: Truncator.py 122 2012-09-17 15:48:58Z kato $

from Population import *
import numpy as np

def KthNearest(D, indices, k):

	sortedD = np.sort(D)
	dmin = sortedD[0, k]
	indices2 = [0]
	for i in indices:
		d = sortedD[i, k]
		if d < dmin:
			indices2 = [i]
			dmin = d
		elif d == dmin:
			indices2.append(i)
	return indices2

def DistanceMatrix(pop, fcoord):

	# Squared-Distance matrix. each row corresponds to an individual, and columns the distance to the neighbors
	D = np.zeros([len(pop), len(pop)])

	for i1 in range(len(pop)):
		o1 = fcoord(pop[i1]) #o1 = pop[i1].Objectives
		for i2 in range(len(pop)):
			if i2 == i1:
				D[i1, i2] = 0.0
				continue
			o2 = fcoord(pop[i2]) #o2 = pop[i2].Objectives
			d = o2 - o1
			d = np.dot(d, d)
			D[i1, i2] = d
	return D

class Truncator(object):

	def __init__(self, space):
		"""
		space is either "OBJECTIVE" or "PARAMETRIC"
		"""

		if space == "OBJECTIVE":
			self.CoordFunc = lambda i: i.Objectives
		elif space == "PARAMETRIC":
			self.CoordFunc = lambda i: i.DesignParameters.AsVector()

	def Truncate(self, pop, N):
		"""
		Truncate the population "pop" until its size is N.
		"""
		truncated = Population(pop)

		while len(truncated) > N:
			D = DistanceMatrix(truncated, self.CoordFunc)
			indices = range(0, D.shape[0])
			for k in range(1, D.shape[1]):
				indices = KthNearest(D, indices, k)
				if len(indices) == 1:
					break
			i = indices[0]
			truncated2 = Population(truncated[:i])
			truncated2.extend(truncated[i + 1:])
			truncated = truncated2

		return truncated

