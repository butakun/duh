# $Id: CartesianGrid.py 66 2010-12-24 07:28:53Z kato $

from Grid import Grid
import numpy as n
import math as m

class CartesianGrid(Grid):

	def __init__(self, shape):

		Grid.__init__(self, shape)
		self.Name = "Cartesian"

	def DistanceSqBetweenNodes(self, node1, node2):

		"""
		dx = float(node1[0] - node2[0]) / self.Shape[0]
		dy = float(node1[1] - node2[1]) / self.Shape[1]
		d = dx * dx + dy * dy
		"""
		ref = n.max(self.Shape)
		dx = float(node1[0] - node2[0]) / ref
		dy = float(node1[1] - node2[1]) / ref
		d = dx * dx + dy * dy
		return d

