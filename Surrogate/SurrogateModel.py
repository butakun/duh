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
# $Id: SurrogateModel.py 50 2010-10-06 15:41:52Z kato $

import numpy as n

class SurrogateModel(object):

	def Train(self, db):
		self.DB = db.Scale()
		self.TrainScaled(self.DB)

	def Evaluate(self, x):
		scaled = self.EvaluateScaled(self.DB.ScaleParameters(x))
		return self.DB.UnscaleResponses(scaled)

