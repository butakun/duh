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

