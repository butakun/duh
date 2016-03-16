# $Id: TorczonMeritFunction.py 88 2011-02-19 19:17:27Z kato $

import numpy as n

class TorczonMeritFunction(object):

	def __init__(self, pop, chromosome, weight, name):

		self.Weight = weight
		self.Name = name # Response name

		self.Update(pop)

		lower = chromosome.DesignParameters.MinAsVector()
		upper = chromosome.DesignParameters.MaxAsVector()
		self.ParameterScales = upper - lower

		print "Torczon: fitness range = ", self.FitnessRange, "parameter scales = ", self.ParameterScales

	def Evaluate(self, v):

		if isinstance(v, list):
			for indi in v:
				self.EvaluateIndi(indi)
		else:
			self.EvaluateIndi(v)

	def EvaluateIndi(self, indi):

		r = indi.Responses.FindByName(self.Name)[0]
		r.Value = self.ComputeMerit(indi)

	def ComputeMerit(self, indi):

		v = indi.DesignParameters.AsVector()

		# Find the nearest pole
		pNearest = self.Poles[0]
		d = v - pNearest
		d /= self.ParameterScales
		distNearest = n.dot(d, d)
		for p in self.Poles[1:]:
			d = v - p
			dist = n.dot(d, d)
			if dist < distNearest:
				distNearest = dist
				pNearest = p

		d = v - pNearest
		d /= self.ParameterScales
		d = n.dot(d, d)

		return self.Weight * self.FitnessRange * d

	def Update(self, pop):

		fits = n.array([ i.Fitness for i in pop ])
		minFitness, maxFitness = fits.min(), fits.max()
		mean, std = fits.mean(), fits.std()
		self.FitnessRange = std
		print "Fitness mean and std = ", mean, std

		self.Poles = []
		for indi in pop:
			self.Poles.append(indi.DesignParameters.AsVector())

