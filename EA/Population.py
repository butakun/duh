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
# $Id: Population.py 112 2012-08-03 05:00:36Z kato $

from Individual import Individual
import StringIO

class Population(list):

	def SortByIncreasingFitness(self):

		self.sort(lambda i1, i2 : cmp(i1.Fitness, i2.Fitness))

	def SortByDecreasingFitness(self):

		self.SortByFitness()

	def SortByFitness(self):

		self.sort(lambda i1, i2 : cmp(i2.Fitness, i1.Fitness))

	def __str__(self):

		sio = StringIO.StringIO()
		for i in self:
			print >>sio, i
		return sio.getvalue()

	def FindByID(self, ID):

		match = filter(lambda i: i.ID == ID, self)
		assert(len(match) == 1)
		return match[0]

	def Randomize(self):

		for i in self:
			i.Randomize()

	def SuccessfulIndividuals(self):

		return Population(filter(lambda i: i.Success == True, self))

	def Filter(self, func):

		return Population(filter(func, self))

