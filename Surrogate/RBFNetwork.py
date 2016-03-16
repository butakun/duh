# $Id: RBFNetwork.py 89 2011-02-19 19:17:38Z kato $

from SurrogateModel import SurrogateModel
import RBF
import numpy as n

class RBFNetwork(SurrogateModel):

	def __init__(self, kernel = RBF.Multiquadric):

		self.__Kernel = kernel
		self.SVDCutOff = 1.0e-15

	def EvaluateScaled(self, x):

		Rho = n.zeros(len(self.HiddenUnits))
		for i, rho in enumerate(self.HiddenUnits):
			Rho[i] = rho.Evaluate(x)
		return n.dot(Rho, self.Weights)

	def TrainScaled(self, db):
		""" db is already scaled. """

		numSamples = len(db)
		numParams = len(db[0][0])
		numResps = len(db[0][1])
		numHiddenUnits = numSamples

		self.HiddenUnits = []
		for sampleIn, sampleOut in db:
			sigma = 1.0
			self.HiddenUnits.append(self.__Kernel(sampleIn, sigma))

		#self.Weights = n.zeros((numSamples, numResps))

		Phi = n.zeros((numSamples, numResps))
		Rho = n.zeros((numSamples, numHiddenUnits))
		for i, sample in enumerate(db):
			sampleIn, sampleOut = sample
			Phi[i, :] = sampleOut
			for j, rho in enumerate(self.HiddenUnits):
				Rho[i, j] = rho.Evaluate(sampleIn)

		#print "Condition number = ", n.linalg.cond(Rho)
		#self.Weights = n.linalg.solve(Rho, Phi)
		try:
			RhoInv = n.linalg.pinv(Rho, self.SVDCutOff)
		except n.linalg.LinAlgError:
			c = n.linalg.cond(Rho)
			print "SVD failed: cond = %e, rcond = %e" % (c, 1.0 / c)
			raise
		self.Weights = n.dot(RhoInv, Phi)

		"""
		RBF Network:
		               N
		    phi(x) = Sigma a_i rho_i(x)
		              i=1 
		Given N training samples whose input vectors are
		    x_i, i = 1, ..., N
		and output vectors
		    y_i, i = 1, ..., N
		(note that x and y are both vectors)
		we construct a linear system of equation
		    [Phi] = [Rho] [a]
		or,
			Phi_ij = y_i^T      (i = 1, ..., N, j = # of outputs)
			Rho_ij = rho_j(x_i) (i = 1, ..., N, j = # of hidden units)
			a_ij = unknown      (i = 1, ..., N, j = # of outputs)
		"""

def Test1D():

	from Database import TestDatabase1D
	import pylab

	db = TestDatabase1D(10, 0.05)
	#db = TestDatabase1D(10, 0.0)
	rbfn = RBFNetwork()
	rbfn.Train(db)
	print rbfn.Weights
	print rbfn.DB.Scaling

	print "Errors at sample points (must be zero)"
	for p, r in db:
		r2 = rbfn.Evaluate(p)
		print p, r, r2, r2 - r

	M = 100
	xx = n.linspace(0.0, 1.0, M)
	yy = n.zeros(M)
	for i in range(M):
		x = n.array([xx[i]])
		yy[i] = rbfn.Evaluate(x)[0]

	yyKernel = n.zeros((len(db), M))
	for i in range(len(db)):
		kernel = rbfn.HiddenUnits[i]
		for j in range(M):
			yyKernel[i, j] = kernel.Evaluate(n.array([xx[j]]))

	xx0 = n.zeros(len(db))
	yy0 = n.zeros(len(db))
	for i, sample in enumerate(db):
		x, y = sample
		xx0[i] = x[0]
		yy0[i] = y[0]

	yy1 = xx * xx + 1.0

	pylab.plot(xx0, yy0, "o")
	pylab.plot(xx, yy)
	#pylab.plot(xx, yy1)
	#for i in range(len(db)):
	#	pylab.plot(xx, yyKernel[i])
	pylab.axis([0.0, 1.0, 0.0, 2.0])
	pylab.show()

if __name__ == "__main__":
	Test1D()

