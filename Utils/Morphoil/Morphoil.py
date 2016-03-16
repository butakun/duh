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
# $Id: Morphoil.py 128 2013-09-21 12:55:31Z kato $

import numpy as np
import scipy.optimize
import math as m
import pickle

def ReadAirfoil(f):

	xys1, xys2 = [], []
	for xys in [xys1, xys2]:
		blankLines = 0
		while True:
			line = f.readline()
			tokens = line.split()
			if len(tokens) == 0:
				blankLines += 1
				if blankLines == 2:
					break
				continue
			x, y = map(float, tokens)
			xys.append([x, y])

	xys1 = np.array(xys1)
	xys2 = np.array(xys2)
	return xys1, xys2

def ReadMorphingNet(f):

	idim, jdim = map(int, f.readline().split())
	PNet = np.zeros((idim, jdim, 2))
	for j in range(jdim):
		for i in range(idim):
			x, y = map(float, f.readline().split())
			PNet[i, j, :] = [x, y]
	return PNet

def ComputeMorphingA0A1(pN1, pN2, pN3, pN4):

	v12 = pN2 - pN1
	v14 = pN4 - pN1
	v13 = pN3 - pN1

	C = np.array([
			[v12[0], v14[0]],
			[v12[1], v14[1]]
			])
	aa = np.linalg.solve(C, v13)
	a0, a1 = aa

	return a0, a1

def MapWithinMorphingCell2(p, pN1, pN2, pN3, pN4):
	"""
	Return the logical coordinates of p within the morphing cell defined by:

	pN4 --- pN3
	 |       |
	pN1 --- pN2

	Note that a logical coordinate outside {0, 1} means that p falls outside the cell.
	"""

	a0, a1 = ComputeMorphingA0A1(pN1, pN2, pN3, pN4)
	y0, y1 = p
	denom = a0 * a1 + a1 * (a1 - 1.0) * y0 + a0 * (a0 - 1.0) * y1
	x0 = a1 * (a0 + a1 - 1.0) * y0 / denom
	x1 = a0 * (a0 + a1 - 1.0) * y1 / denom
	return np.array([x0, x1])

def MorphToMorphingCell(pl, pN1, pN2, pN3, pN4):
	"""
	Returns the physical coordinates of pl withint the morphing cell defined by pN1, ..., pN4.
	"""

	A = pN1 - pN2 - pN4 + pN3
	B = -pN1 + pN2
	C = -pN1 + pN4
	D = pN1
	xi, eta = pl
	p = A * xi * eta + B * xi + C * eta + D
	return p

def MapFunc(pl, pTarget, pN1, pN2, pN3, pN4):
	d = MorphToMorphingCell(pl, pN1, pN2, pN3, pN4) - pTarget
	return np.dot(d, d)

def ContainedWithinMorphingCell(p, pN1, pN2, pN3, pN4):

	v1p = p - pN1
	v12 = pN2 - pN1
	if (np.cross(v12, v1p) < 0.0):
		return False
	v14 = pN4 - pN1
	if (np.cross(v1p, v14) < 0.0):
		return False
	v3p = p - pN3
	v32 = pN2 - pN3
	if (np.cross(v3p, v32) < 0.0):
		return False
	v34 = pN4 - pN3
	if (np.cross(v34, v3p) < 0.0):
		return False
	return True


def MapWithinMorphingCell(p, pN1, pN2, pN3, pN4, ptol = 1e-4):
	"""
	Return the logical coordinates of p within the morphing cell defined by:

	pN4 --- pN3
	 |       |
	pN1 --- pN2

	Note that a logical coordinate outside {0, 1} means that p falls outside the cell.
	"""

	pl0 = np.array([0.5, 0.5])
	f = lambda pl: MapFunc(pl, p, pN1, pN2, pN3, pN4)
	pl = scipy.optimize.fmin(f, pl0, xtol = 1.0e-8, ftol = ptol * ptol, disp = False)
	return pl

def CellOutlierDistance(pl):

	d = pl * (pl < 0.0) + pl * (1.0 < pl)
	d = abs(d)
	return max(d)

def MapToLogicalSpace(PP, PNet):
	"""
	Return pL which contains the logical coordinates of p
	pp is a list of p
	"""

	PL = np.zeros(PP.shape)

	imin = 0
	imax = PNet.shape[0] - 1
	jmin = 0
	jmax = PNet.shape[1] - 1

	derr = np.zeros(PP.shape[0])
	derr[:] = 1.0e5

	npts = len(PP)
	for l, p in enumerate(PP):
		found = False
		for i in range(0, imax):
			for j in range(0, jmax):
				dnet = np.array([float(i), float(j)])
				pN1 = PNet[i, j, :]
				pN2 = PNet[i + 1, j, :]
				pN3 = PNet[i + 1, j + 1, :]
				pN4 = PNet[i, j + 1, :]
				pl = MapWithinMorphingCell(p, pN1, pN2, pN3, pN4)
				#print "Cell %d, %d: pl = %f, %f" % (i, j, pl[0], pl[1])
				if 0.0 <= pl[0] and pl[0] <= 1.0 and 0.0 <= pl[1] and pl[1] <= 1.0:
					PL[l, :] = pl + dnet
					found = True
					derr[l] = 0.0
					break
				d = CellOutlierDistance(pl)
				if d < derr[l]:
					PL[l, :] = pl + dnet
					derr[l] = d
			if found:
				break
		if found:
			print "Point %d of %d = (%f, %f) mapped to %f, %f" % (l, npts, p[0], p[1], PL[l, 0], PL[l, 1])
		else:
			print "Point %d of %d = (%f, %f) mapped to %f, %f (guess)" % (l, npts, p[0], p[1], PL[l, 0], PL[l, 1])

	return PL

def MapToPhysicalSpace(PL, PNet):

	PP = np.zeros(PL.shape)
	idim, jdim = PNet.shape[0:2]

	for l, pl in enumerate(PL):
		i, j = map(int, pl)
		i = max(0, min(idim - 2, i))
		j = max(0, min(jdim - 2, j))
		print l, pl, i, j
		pN1 = PNet[i, j, :]
		pN2 = PNet[i + 1, j, :]
		pN3 = PNet[i + 1, j + 1, :]
		pN4 = PNet[i, j + 1, :]
		pll = pl - np.array([float(i), float(j)])
		pp = MorphToMorphingCell(pll, pN1, pN2, pN3, pN4)
		PP[l, :] = pp

	return PP

def Save(f, PP, PNet):

	for i in range(len(PP)):
		print >>f, PP[i, 0], PP[i, 1]
	print >>f
	print >>f
	for j in range(PNet.shape[1] - 1):
		for i in range(PNet.shape[0] - 1):
			print >>f, PNet[i, j, 0], PNet[i, j, 1]
			print >>f, PNet[i + 1, j, 0], PNet[i + 1, j, 1]
			print >>f, PNet[i + 1, j + 1, 0], PNet[i + 1, j + 1, 1]
			print >>f, PNet[i, j + 1, 0], PNet[i, j + 1, 1]
			print >>f, PNet[i, j, 0], PNet[i, j, 1]
			print >>f

def SaveAirfoil(f, PP1, PP2, PNet = None):

	for PP in [PP1, PP2]:
		for i in range(len(PP)):
			print >>f, PP[i, 0], PP[i, 1]
		print >>f
		print >>f

	if PNet:
		for j in range(PNet.shape[1] - 1):
			for i in range(PNet.shape[0] - 1):
				print >>f, PNet[i, j, 0], PNet[i, j, 1]
				print >>f, PNet[i + 1, j, 0], PNet[i + 1, j, 1]
				print >>f, PNet[i + 1, j + 1, 0], PNet[i + 1, j + 1, 1]
				print >>f, PNet[i, j + 1, 0], PNet[i, j + 1, 1]
				print >>f, PNet[i, j, 0], PNet[i, j, 1]
				print >>f

def Map(morphingNetFileName, airfoilFileName):

	PNet = ReadMorphingNet(open(morphingNetFileName))
	print "Morphing Net Dimensions = ", PNet.shape
	PP1, PP2 = ReadAirfoil(open(airfoilFileName))

	print "Mapping the first curve"
	PL1 = MapToLogicalSpace(PP1, PNet)
	print "Mapping the second curve"
	PL2 = MapToLogicalSpace(PP2, PNet)

	pickle.dump([PL1, PL2], open("mapping.pickled", "w"))
	print "Physical-to-logical space mapping saved to mapping.pickled"

	SaveAirfoil(open("ref.dat", "w"), PP1, PP2, PNet)

def Morph(morphingNetFileName, mappingFileName):

	PNet = ReadMorphingNet(open(morphingNetFileName))
	PL1, PL2 = pickle.load(open(mappingFileName))

	PP1 = MapToPhysicalSpace(PL1, PNet)
	PP2 = MapToPhysicalSpace(PL2, PNet)

	#SaveAirfoil(open("morphed.dat", "w"), PP1, PP2, PNet)
	SaveAirfoil(open("morphed.dat", "w"), PP1, PP2)

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 4:
		print "python %s map MorphingNet.dat Airfoil.dat" % (sys.argv[0])
		print "python %s morph MorphingNet.dat mapping.pickled" % (sys.argv[0])
	elif sys.argv[1] == "map":
		Map(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "morph":
		Morph(sys.argv[2], sys.argv[3])
	else:
		raise ValueError

