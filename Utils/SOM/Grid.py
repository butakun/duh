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

