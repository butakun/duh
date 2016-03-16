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

