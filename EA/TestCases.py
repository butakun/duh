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
# $Id: TestCases.py 113 2012-08-03 07:54:46Z kato $

from Individual import Individual
from Value import Value
from BoundedValue import BoundedValue
from PenaltyEvaluator import *
import numpy as np
import math as m

class TestCase(object):

	def __call__(self, indi):
		return self.Function(indi)

class Rosenbrock(TestCase):

	def __init__(self, dim = 2):
		self.Dim = 2

	def Chromosome(self):

		indi = Individual()
		for i in range(self.Dim):
			ii = i + 1
			#indi.DesignParameters.append(BoundedValue("X%d" % ii, "FLOAT", 0.2, 1.0, -10.0, 10.0))
			indi.DesignParameters.append(BoundedValue("X%d" % ii, "FLOAT", 0.2, 1.0, -2.0, 2.0))

		indi.Responses.append(Value("F", "FLOAT", None))

		return indi

	def Function(self, indi):

		f = 0.0
		for i in range(self.Dim - 1):
			x = indi.DesignParameters[i].Value
			y = indi.DesignParameters[i + 1].Value
			f += (1.0 - x) * (1.0 - x) + 100.0 * (y - x * x) * (y - x * x)
		indi.Responses[0].Value = f
		indi.Success = True
		return indi

	def Objectives(self):

		return [Penalty("MINIMIZE", "F")]

	def Constraints(self):

		return []

class RosenbrockUncomputable(Rosenbrock):

	def __init__(self):
		Rosenbrock.__init__(self, dim = 2)

	def Function(self, indi):

		assert(self.Dim == 2)

		f = 0.0
		x = indi.DesignParameters[0].Value
		y = indi.DesignParameters[1].Value
		f += (1.0 - x) * (1.0 - x) + 100.0 * (y - x * x) * (y - x * x)
		indi.Responses[0].Value = f
		indi.Success = (x + y) <= 1.0
		return indi

class ZDT1(TestCase):

	def __init__(self, dim = 2):
		self.Dim = 2

	def Chromosome(self):

		indi = Individual()
		for i in range(self.Dim):
			indi.DesignParameters.append(BoundedValue("X%d" % (i + 1), "FLOAT", 0.5, 1.0, 0.0, 1.0))

		indi.Responses.append(Value("F1", "FLOAT", None))
		indi.Responses.append(Value("F2", "FLOAT", None))

		return indi

	def Function(self, indi):

		N = self.Dim
		X = indi.DesignParameters.AsVector()

		F1 = X[0]
		g = 1.0 + 9.0 / (N - 1.0) * X[1:].sum()
		F2 = g * (1.0 - m.sqrt(F1 / g))

		indi.Responses[0].Value = F1
		indi.Responses[1].Value = F2
		indi.Success = True

		return indi

	def Objectives(self):

		return [Penalty("MINIMIZE", "F1"), Penalty("MINIMIZE", "F2")]

	def Constraints(self):

		return []

class ZDT2(ZDT1):

	def __init__(self, dim = 2):
		ZDT1.__init__(self, dim)

	def Function(self, indi):

		N = self.Dim
		X = indi.DesignParameters.AsVector()

		F1 = X[0]
		g = 1.0 + 9.0 / (N - 1.0) * X[1:].sum()
		F2 = g * (1.0 - pow(F1 / g, 2))

		indi.Responses[0].Value = F1
		indi.Responses[1].Value = F2
		indi.Success = True

		return indi

class ZDT3(ZDT1):

	def __init__(self, dim = 2):
		ZDT1.__init__(self, dim)

	def Function(self, indi):

		N = self.Dim
		X = indi.DesignParameters.AsVector()

		F1 = X[0]
		g = 1.0 + 9.0 / (N - 1.0) * X[1:].sum()
		F2 = g * (1.0 - m.sqrt(F1 / g) - (F1 / g) * m.sin(10.0 * m.pi * F1))

		indi.Responses[0].Value = F1
		indi.Responses[1].Value = F2
		indi.Success = True

		return indi

