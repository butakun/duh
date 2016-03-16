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
# $Id: BoundedValue.py 11 2010-04-08 14:50:05Z kato $

from Value import Value
import random

class BoundedValue(Value):

	def __init__(self, name, valueType, value, refValue, minValue, maxValue):

		Value.__init__(self, name, valueType, value, refValue)
		self.MinValue = minValue
		self.MaxValue = maxValue
		assert(self.MinValue < self.MaxValue)
		assert(self.MinValue <= self.RefValue and self.RefValue <= self.MaxValue)

	def ClipWithinBounds(self):

		self.Value = min(self.MaxValue, max(self.Value, self.MinValue))

	def Randomize(self):

		r = random.random()
		self.Value = (1.0 - r) * self.MinValue + r * self.MaxValue

