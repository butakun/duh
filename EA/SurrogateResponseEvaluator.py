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
# $Id: SurrogateResponseEvaluator.py 83 2011-02-03 16:05:19Z kato $

from PopulationEvaluator import PopulationEvaluator

class SurrogateResponseEvaluator(PopulationEvaluator):

	def __init__(self, responseModel, successModel, chromosome):

		self.ResponseSurrogate = responseModel
		self.SuccessSurrogate = successModel
		self.Chromosome = chromosome

	def Function(self, indi):

		x = indi.DesignParameters.AsVector()
		y = self.ResponseSurrogate.Evaluate(x)
		s = self.SuccessSurrogate.Evaluate(x)

		for i, v in enumerate(y):
			indi.Responses[i].Value = v

		indi.Success = s > 0.5

