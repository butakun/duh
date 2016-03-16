# $Id: SOM.py 66 2010-12-24 07:28:53Z kato $

import numpy as n
import math as m

class SOM(object):

	"""
	Self-Organizing Map (Kohonen Map)
	"""

	def __init__(self, grid, N, scale, distFunc):
		""" N = dimension of the training sample vector """

		self.Grid = grid
		self.W = n.zeros([grid.Shape[0], grid.Shape[1], N])
		self.N = N
		self.Scale = n.array(scale)
		self.DistFunc = distFunc

		self.__InitWeights()

		self.W = self.W * self.Scale

		self.__PrecomputeDistanceMatrix()

	def FindBMU(self, input):
		""" Find the Best Matching Unit (BMU), returns the (i, j) index and the Eucledean distance. """

		dmin = self.DistanceSq(self.W[0, 0], input)
		ijmin = (0, 0)
		for j in range(self.W.shape[1]):
			for i in range(self.W.shape[0]):
				d = self.DistanceSq(self.W[i, j, :], input)
				if d < dmin:
					dmin = d
					ijmin = (i, j)

		return ijmin, m.sqrt(dmin)

	def Train(self, sample, alpha):
		""" sample - input vector, alpha - learning rate """

		bmu, d = self.FindBMU(sample)
		#theta = self.Grid.Neighborhood(bmu, self.DistFunc)
		f = n.frompyfunc(self.DistFunc, 1, 1)
		theta = f(self.DistMat[bmu])
		theta = theta.reshape(theta.shape[0], theta.shape[1], 1)
		dW = sample - self.W
		self.W = self.W + alpha * theta * dW

	def DistanceSq(self, w1, w2):

		d = w1 / self.Scale - w2 / self.Scale
		d = n.dot(d, d)
		return d

	def __InitWeights(self):
		"""
		Initialize the weight vectors.
		"""
		idim, jdim = self.W.shape[0:2]
		for d in range(self.W.shape[2]):
			corner = d % 4
			if corner == 0:
				ij0, ci, cj = (0.0, 0.0), 1.0, 1.0
			elif corner == 1:
				ij0, ci, cj = (1.0, 0.0), -1.0, 1.0
			elif corner == 2:
				ij0, ci, cj = (1.0, 1.0), -1.0, -1.0
			elif corner == 3:
				ij0, ci, cj = (0.0, 1.0), 1.0, -1.0

			for i in range(idim):
				ii = float(i) / float(idim - 1)
				for j in range(jdim):
					jj = float(j) / float(jdim - 1)
					di = ii - ij0[0]
					dj = jj - ij0[1]
					self.W[i, j, d] = m.exp(-0.5 * (di * di + dj * dj))

	def __PrecomputeDistanceMatrix(self):

		self.DistMat = n.zeros((self.Grid.Shape[0], self.Grid.Shape[1], self.Grid.Shape[0], self.Grid.Shape[1]))
		for ic in range(self.Grid.Shape[0]):
			for jc in range(self.Grid.Shape[1]):
				for i in range(self.Grid.Shape[0]):
					for j in range(self.Grid.Shape[1]):
						self.DistMat[ic, jc, i, j] = self.Grid.DistanceSqBetweenNodes((ic, jc), (i, j))

