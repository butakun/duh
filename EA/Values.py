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
# $Id: Values.py 131 2014-01-01 13:57:57Z kato $

import numpy

class Values(list):

	def AsVector(self):

		return numpy.array([ i.Value for i in self ])

	def SetToVector(self, vec):

		for i in range(len(self)):
			self[i].Value = vec[i]

	def MinAsVector(self):

		return numpy.array([ i.MinValue for i in self ])

	def MaxAsVector(self):

		return numpy.array([ i.MaxValue for i in self ])

	def SetMinToVector(self, vec):

		for i in range(len(self)):
			self[i].MinValue = vec[i]

	def SetMaxToVector(self, vec):

		for i in range(len(self)):
			self[i].MaxValue = vec[i]

	def FindByName(self, name):

		return filter(lambda v: v.Name == name, self)

	def Initialize(self):
		""" Initialize the values to their respective reference values """
		for v in self:
			v.Value = v.RefValue

	def __getitem__(self, i):

		if isinstance(i, int):
			return list.__getitem__(self, i)
		return self.FindByName(i)[0]

	def __str__(self):

		return "[" + reduce(lambda x, y: x + " " + y, map(lambda v: str(v.Value), self)) + "]"

