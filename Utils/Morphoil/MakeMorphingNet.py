import math as m
import numpy as np
import scipy.interpolate

class BSpline(object):

	def __init__(self, cps):

		t = np.linspace(0.0, len(cps) - 1, len(cps))

		self.Cps = np.array(cps).transpose()
		if self.Cps.shape[1] < 4:
			print "WARNING: # of control points < 4, we will resort to k = 2, which is not recomended"
			k = 2
		else:
			k = 3 # by default we use a cubic b-spline
		tck, u = scipy.interpolate.splprep(self.Cps, k = k, u = t, s = 0.0)
		self.TCK = tck
		self.U = u

	def EvaluateAt(self, t):

		p = scipy.interpolate.splev(t, self.TCK)
		return p

def ReadControlPoints(f):

	N, M = map(int, f.readline().split())
	CP = np.zeros((N, M, 2))
	for j in range(M):
		for i in range(N):
			CP[i, j, :] = map(float, f.readline().split())
	return CP

def MakeNet(CP, splitsN, splitsM):
	"""
	splits each cell into "splitsN" x "splitsM" subcells.
	"""

	N, M = CP.shape[0:2]
	PNet = np.zeros(((N - 1) * splitsN + 1, (M - 1) * splitsM + 1, 2))
	print "Net dims = ", PNet.shape

	SplineClass = BSpline
	splines = []
	for j in range(M):
		spline = SplineClass(CP[:, j, :])
		splines.append(spline)

	for j in range(M):
		for i in range(N - 1):
			for l in range(splitsN):
				t = float(i) + float(l) / float(splitsN)
				print i, j, l, t
				p = splines[j].EvaluateAt(t)
				PNet[splitsN * i + l, splitsM * j, :] = p
		PNet[-1, splitsM * j, :] = splines[j].EvaluateAt(float(N - 1))

	for j in range(M - 1):
		for l in range(1, splitsM):
			eta = float(l) / float(splitsM)
			PNet[:, splitsM * j + l, :] = (1.0 - eta) * PNet[:, splitsM * j, :] + eta * PNet[:, splitsM * (j + 1), :]

	return PNet

def DumpNet(f, pp):

	for j in range(pp.shape[1]):
		for i in range(pp.shape[0]):
			print >>f, pp[i, j, 0], pp[i, j, 1]
		print >>f

def SaveMorphingNet(f, pp):

	print >>f, pp.shape[0], pp.shape[1]
	for j in range(pp.shape[1]):
		for i in range(pp.shape[0]):
			print >>f, pp[i, j, 0], pp[i, j, 1]

def Main(cpfilename, outfilename):

	#spine = np.array(SPINE)

	CP = ReadControlPoints(open(cpfilename))
	DumpNet(open("net_cp.dat", "w"), CP)

	PNet = MakeNet(CP, 10, 6)
	DumpNet(open("net.dat", "w"), PNet)

	SaveMorphingNet(open(outfilename, "w"), PNet)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 3:
		print "python %s NetControlPoints.dat MorphingNet.dat" % sys.argv[0]
	else:
		Main(sys.argv[1], sys.argv[2])

