# $Id: SOMUtils.py 66 2010-12-24 07:28:53Z kato $

from Backbone import ExperimentPlan
import numpy as n

def FindValues(exp, names):

	values = []
	for name in names:
		values.append(exp.Value(name)["Value"])
	return values

def ExtractSOMSamples(plan, names):
	""" Extract parameters/responses from "names" """

	#plan2 = plan.ApplyFilter(lambda e: e["Status"] == "DONE" and e["Success"])
	plan2 = filter(lambda e: e.Status == "DONE" and e.IsSuccess(), plan)

	samples = []
	for exp in plan2:
		values = FindValues(exp, names)
		samples.append((exp.ID, values))

	return samples

def BMUs(som, samples):

	bmus = []
	for id, sample in samples:
		ij, d = som.FindBMU(sample)
		bmus.append((id, ij))
	return bmus

def ExportSOM(f, som, names, samples):

	bmus = BMUs(som, samples)

	print >> f, "# Self-Organizing Map"
	print >> f, "# Grid Topology"
	print >> f, som.Grid.Name
	print >> f, "# Grid Shape"
	print >> f, som.Grid.Shape[0], "\t", som.Grid.Shape[1]
	print >> f, "# Variable Names"
	print >> f, reduce(lambda a, b: a + "\t" + b, names)
	print >> f, "# Weights"
	for i in range(som.Grid.Shape[0]):
		for j in range(som.Grid.Shape[1]):
			w = som.W[i, j, :]
			buf = reduce(lambda a, b: a + "\t" + b, map(lambda a: "%20.12e" % a, w))
			print >> f, buf
	print >> f, "# Best Matching Units"
	for bmu in bmus:
		print >> f, "%d\t%d\t%d" % (bmu[0], bmu[1][0], bmu[1][1])

def ImportSOM(f):

	line = f.readline().strip()
	if line != "# Self-Organizing Map":
		print "This is not a SOM data file"
		raise Exception

	f.readline()
	topology = f.readline().split()[0]
	f.readline()
	dim1, dim2 = map(int, f.readline().split())
	shape = (dim1, dim2)
	f.readline()
	names = f.readline().split()
	f.readline()
	W = []
	for i in range(shape[0]):
		Wj = []
		for j in range(shape[1]):
			w = map(float, f.readline().split())
			Wj.append(w)
		W.append(Wj)
	W = n.array(W)
	f.readline()
	bmus = []
	while True:
		buf = f.readline().split()
		if not buf:
			break
		id, i, j = map(int, buf)
		bmus.append((id, (i, j)))

	return topology, shape, names, W, bmus

"""
def HierarchicalClustering(som):

	W = som.W
	IDIM, JDIM = W.shape

	clusters = []

	for i in range(IDIM):
		for j in range(JDIM):
"""

