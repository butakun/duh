# $Id: Dominance.py 112 2012-08-03 05:00:36Z kato $

import numpy as n

class Dominance(object):

	def __init__(self):

		pass

	def FirstDominatesSecond(self, indi1, indi2):

		f1 = indi1.IsFeasible()
		f2 = indi2.IsFeasible()
		if not f1 and f2:
			return False
		elif f1 and not f2:
			return True
		elif f1 and f2:
			o1 = indi1.Objectives
			o2 = indi2.Objectives
			return n.all(o1 <= o2) and n.any(o1 < o2)
		else:
			c1 = indi1.Constraints
			c2 = indi2.Constraints
			return n.all(c1 < c2)

