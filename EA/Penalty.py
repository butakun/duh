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
# $Id: Penalty.py 82 2011-02-03 15:54:15Z kato $

from Individual import Individual

class Penalty(object):

	def __init__(self, type, valueName, weight = 1.0, ref = 1.0, imposed = 0.0, exponent = 1):
		"""
		P(x) = Weight * ((x - imposed) / ref)^exponent
		"""

		self.Type = type
		self.ValueName = valueName
		self.Weight = weight
		self.ReferenceValue = ref
		self.ImposedValue = imposed
		self.Exponent = exponent

	def Apply(self, indi):

		if self.ValueName == "__SUCCESS__":
			value = float(indi.Success)
		else:
			value = indi.Responses.FindByName(self.ValueName)[0].Value

		if self.Type == "MINIMIZE":
			p = self.Weight * pow((value - self.ImposedValue) / self.ReferenceValue, self.Exponent)
		elif self.Type == "MAXIMIZE":
			p = self.Weight * pow((self.ImposedValue - value) / self.ReferenceValue, self.Exponent)
		elif self.Type == "LOWER_BOUND":
			p = self.Weight * pow(max(0.0, self.ImposedValue - value) / self.ReferenceValue, self.Exponent)
		elif self.Type == "UPPER_BOUND":
			p = self.Weight * pow(max(0.0, value - self.ImposedValue) / self.ReferenceValue, self.Exponent)
		else:
			raise Exception("Unknown penalty type %s" % self.Type)
		return p

