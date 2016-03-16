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
$Id$

from Population import Population
import numpy as np

class DensityFilter(object):
	"""
	Evaluates the density distribution of a foreground population
	w.r.t. a background population. The usage is to filter individuals
	in the new population (foreground) that are too close to the existing
	population (background).
	"""

	def __init__(self, bgPop):
		# bgPop ... background population
		self.BGPop = bgPop

	def Evaluate(self, fgPop):

