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
# $Id: Database.py 84 2011-02-08 02:25:48Z kato $

import numpy as n

class Database(list):

	def __init__(self, scaling = None):
		self.Scaling = scaling

	def Scale(self):
		P, R = self.Matrices()
		minP, maxP = P.min(0), P.max(0)
		minR, maxR = R.min(0), R.max(0)
		paramRange = [minP, maxP]
		respRange = [minR, maxR]
		scaling = {"ParameterRange":paramRange, "ResponseRange":respRange}
		scaled = Database(scaling)

		# avoid having zeros in the denominator. this can happen when all sample has the same response value.
		# e.g., success flags (all ones or all zeros are quire possible)
		refR = maxR - minR
		refR[refR == 0] = 1.0

		for p, r in self:
			p2 = (p - minP) / (maxP - minP)
			r2 = (r - minR) / refR
			scaled.append([p2, r2])
		return scaled

	def Matrices(self):
		P, R = [], []
		for p, r in self:
			P.append(p)
			R.append(r)
		P = n.array(P)
		R = n.array(R)
		return P, R

	def ScaleParameters(self, p):
		minP, maxP = self.Scaling["ParameterRange"]
		return (p - minP) / (maxP - minP)

	def UnscaleResponses(self, r):
		minR, maxR = self.Scaling["ResponseRange"]
		return r * (maxR - minR) + minR

def TestDatabase1D(N, eps):
	db = Database()
	for i in range(N):
		x = n.random.random()
		#x = float(i) / float(N - 1)
		noise = eps * (n.random.random() - 0.5)
		y = x * x + 1.0 + noise
		db.append([n.array([x]), n.array([y])])
	return db

