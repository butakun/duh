# $Id: InitControlPoints.py 107 2012-05-24 10:49:22Z kato $

import numpy as np
import math as m

"""
SPINE = [
	[0.0, 0.0],
	[2.2, 3.0],
	[5.0, 2.8],
	[7.28807241172, -1.25086260267]
	]

#SLOPE = [53.75, 29.25, -39.88, -60.54]
SLOPE = [53.75, 20.0, -25.0, -60.54]

THICK = [ 1.0, 4.0, 4.0, 1.0 ]
"""

def ReadControlPointsLayout(f):

	f.readline()
	N = int(f.readline())
	spine = []
	for i in range(N):
		x, y = map(float, f.readline().split())
		spine.append([x, y])
	spine = np.array(spine)
	f.readline()
	slope = []
	for i in range(N):
		slope.append(float(f.readline()))
	f.readline()
	thick = []
	for i in range(N):
		thick.append(float(f.readline()))

	return spine, slope, thick

def MakeControlPoints(spine, slope, thick):

	N = spine.shape[0]
	M = 3

	CP = np.zeros((N, M, 2))

	for i in range(N):
		ip = min(N - 1, i + 1)
		im = max(0, i - 1)
		p = spine[i, :]
		"""
		vt = spine[ip, :] - spine[im, :]
		vt = vt / m.sqrt(np.dot(vt, vt))
		"""
		theta = m.radians(slope[i])
		print i, slope[i], theta
		vt = np.array([m.cos(theta), m.sin(theta)])
		vn = np.array([-vt[1], vt[0]])
		CP[i, 0, :] = p - 0.5 * thick[i] * vn
		CP[i, 1, :] = p
		CP[i, 2, :] = p + 0.5 * thick[i] * vn

	return CP

def SaveControlPointsGNUPlot(f, CP):

	N, M = CP.shape[0:2]
	for j in range(M):
		for i in range(N):
			print >>f, CP[i, j, 0], CP[i, j, 1]
		print >>f

def SaveControlPoints(f, CP):

	N, M = CP.shape[0:2]
	print >>f, N, M
	for j in range(M):
		for i in range(N):
			print >>f, CP[i, j, 0], CP[i, j, 1]

def Main(layoutFileName, outFileName):

	spine, slope, thick = ReadControlPointsLayout(open(layoutFileName))
	CP = MakeControlPoints(spine, slope, thick)

	SaveControlPoints(open(outFileName, "w"), CP)
	SaveControlPointsGNUPlot(open("cp_gnuplot.dat", "w"), CP)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 3:
		print "Usage: python %s LayoutFileName ControlPoints.dat" % sys.argv[0]
	else:
		Main(sys.argv[1], sys.argv[2])

