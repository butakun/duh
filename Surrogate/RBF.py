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

