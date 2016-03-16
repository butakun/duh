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
# $Id: RBF.py 25 2010-07-14 15:37:33Z kato $

import numpy as n
import math as m

class Gaussian(object):

	def __init__(self, center, sigma):
		""" Gaussian centered at xc with standard deviation of sigma """
		self.center = center
		self.var = sigma * sigma

	def Evaluate(self, x):
		dx = x - self.center
		dxsq = n.dot(dx, dx)
		return m.exp(-dxsq / (2.0 * self.var))

class Multiquadric(object):

	def __init__(self, center, sigma):
		""" Multiquadric kernel """
		self.center = center
		self.var = sigma * sigma

	def Evaluate(self, x):
		dx = x - self.center
		dxsq = n.dot(dx, dx)
		return m.sqrt((self.var + dxsq) / self.var)

