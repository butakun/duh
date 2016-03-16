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

