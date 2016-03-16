# $Id: Grid.py 66 2010-12-24 07:28:53Z kato $

import numpy as n

class Grid(object):

	def __init__(self, shape):

		self.Shape = shape

	def DistanceSqBetweenNodes(self, node1, node2):

		raise Exception

	def Neighborhood(self, ijc, distFunc):
		""" Neighborhood function values around the node ijc """

		D = n.zeros(self.Shape)
		for j in range(self.Shape[1]):
			for i in range(self.Shape[0]):
				dsq = self.DistanceSqBetweenNodes(ijc, (i, j))
				D[i, j] = distFunc(dsq)

		return D

