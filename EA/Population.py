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

