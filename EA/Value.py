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
# $Id: Value.py 88 2011-02-19 19:17:27Z kato $

class Value(object):

	def __init__(self, name, valueType, value = 0.0, refValue = 1.0):
		"""
		valueType = "FLOAT" | "INTEGER" | ...
		"""

		self.Name = name
		self.Type = valueType
		self.Value = value
		self.RefValue = refValue

	def __str__(self):

		return "Name:%s, Type:%s, Value:%f, RefValue:%f" % (self.Name, self.Type, self.Value, self.RefValue)

