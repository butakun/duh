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

