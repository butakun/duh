# $Id: SOMView.py 106 2012-01-25 10:03:09Z kato $

import SOMUtils
import pylab
import numpy as n

def CartesianBMUMarkers(W, bmus):

	M = {}
	for id, ij in bmus:
		M[ij] = id
	return M

def CartesianGridView(varNames, shape, names, W, bmus):

	markers = CartesianBMUMarkers(W, bmus)

	if len(varNames) == 1:
		name = varNames[0]
		I = -1
		for i in range(len(names)):
			if name == names[i]:
				I = i
				break
		assert(I >= 0)

		pylab.imshow(W[:, :, I], interpolation = "nearest")
		markerColor = "white"
	else:
		dims = len(names)
		mins = n.zeros(dims)
		scales = n.ones(dims)
		for i in range(dims):
			vmin = n.min(W[:, :, i])
			vmax = n.max(W[:, :, i])
			mins[i] = vmin
			if vmax <= vmin:
				scales[i] = 1.0
			else:
				scales[i] = vmax - vmin

		rgbs = (W[:, :, :] - mins) / scales
		if W.shape[2] < 3:
			one = n.ones((W.shape[0], W.shape[1], 3))
			one[:, :, 0:2] = rgbs[:, :, 0:2]
			rgbs = one
		else:
			rgbs = rgbs[:, :, 0:3]
		pylab.imshow(rgbs, interpolation = "nearest")
		markerColor = "black"

	for ij, id in markers.items():
		pylab.text(
			ij[1], ij[0], "%d" % id,
			color = markerColor,
			horizontalalignment = "center",
			fontsize = "8"
			)

def HexagonalGridView(varNames, shape, names, W, bmus):

	markers = CartesianBMUMarkers(W, bmus)

	X = n.array(range(shape[0]) * shape[1], float).reshape(shape)
	Y = n.array(range(shape[1]) * shape[0], float).reshape(shape[1], shape[0]).transpose()

	S = n.ones(shape[0] * shape[1]) * 500

	for i in range(shape[0]):
		if i % 2 == 1:
			X[i, :] -= 0.5

	X = X.reshape(shape[0] * shape[1])
	Y = Y.reshape(shape[0] * shape[1])

	# Normalize the weights
	dims = len(names)
	mins = n.zeros(dims)
	scales = n.ones(dims)
	for i in range(dims):
		vmin = n.min(W[:, :, i])
		vmax = n.max(W[:, :, i])
		mins[i] = vmin
		if vmax <= vmin:
			scales[i] = 1.0
		else:
			scales[i] = vmax - vmin

	Wn = n.array(W)
	Wn -= mins
	Wn /= scales

	if len(varNames) == 1:
		name = varNames[0]
		I = -1
		for i in range(len(names)):
			if name == names[i]:
				I = i
				break
		assert(I >= 0)

		C = n.ones((shape[0] * shape[1], 3))
		C[:, 0] = Wn[:, :, I].reshape(shape[0] * shape[1])
		C[:, 1] = C[:, 0]
		C[:, 2] = C[:, 0]
		markerColor = "white"
		markerColor = "red"
	else:
		C = n.ones((shape[0] * shape[1], 3))
		for i in range(Wn.shape[2]):
			C[:, i] = Wn[:, :, i].reshape(shape[0] * shape[1])

		markerColor = "black"

	pylab.scatter(X, Y, S, C, "h")

	for ij, id in markers.items():
		i, j = map(float, ij)
		if ij[0] % 2 == 1:
			j -= 0.5
		i -= 0.4
		pylab.text(
			j, i, "%d" % id,
			color = markerColor,
			horizontalalignment = "center",
			fontsize = "8"
			)

def Main(filename, varNames):

	topology, shape, names, W, bmus = SOMUtils.ImportSOM(open(filename))
	print topology
	if topology == "Cartesian":
		CartesianGridView(varNames, shape, names, W, bmus)
	elif topology == "Hexagonal":
		HexagonalGridView(varNames, shape, names, W, bmus)

	pylab.axis([-1.5, shape[0], -1.5, shape[1]])
	pylab.axis("off")

	pylab.show()

if __name__ == "__main__":

	import sys
	Main(sys.argv[1], sys.argv[2:])

