# $Id: SurrogateModel.py 50 2010-10-06 15:41:52Z kato $

import numpy as n

class SurrogateModel(object):

	def Train(self, db):
		self.DB = db.Scale()
		self.TrainScaled(self.DB)

	def Evaluate(self, x):
		scaled = self.EvaluateScaled(self.DB.ScaleParameters(x))
		return self.DB.UnscaleResponses(scaled)

