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

