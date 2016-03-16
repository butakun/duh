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
# $Id: HexagonalGrid.py 66 2010-12-24 07:28:53Z kato $

from Grid import Grid
import numpy as n

class HexagonalGrid(Grid):
	"""
	4x6 hex grid looks like this:
	 o o o o o o
	o o o o o o
	 o o o o o o
	o o o o o o
	"""

	def __init__(self, shape):

		Grid.__init__(self, shape)

		Grid.Name = "Hexagonal"

		# Set up the rotated coordinate system
		# See http://www-acaps.cs.mcgill.ca/~clump/hexes.txt
		self.Coord = n.zeros((shape[0], shape[1], 2), int)
		for i in range(shape[0]):
			for j in range(shape[1]):
				self.Coord[i, j, :] = (i, j)
		for i in range(shape[0]):
			self.Coord[i, :, 1] += i / 2

	def DistanceSqBetweenNodes(self, node1, node2):

		irow = node1[0] % 2

		dx = node2[0] - node1[0]
		dy = node2[1] - node1[1]

		if (dx >= 0 and dy >= 0) or (dx < 0 and dy < 0):
			d = max(abs(dx), abs(dy))
		else:
			d = abs(dx) + abs(dy)
		d = d / float(n.max(self.Shape))
		return d * d

def Test():

	g = HexagonalGrid((5, 5))
	c = g.Coord
	print c[:, :, 0] * 10 + c[:, :, 1]

if __name__ == "__main__":
	Test()

