import Backbone
import numpy as np
import math as m

def ZDT3(exp):

	x1 = exp.Parameter("X1")["Value"]
	x2 = exp.Parameter("X2")["Value"]
	X = np.array([x1, x2])

	N = 2
	F1 = X[0]
	g = 1.0 + 9.0 / (N - 1.0) * X[1:].sum()
	F2 = g * (1.0 - m.sqrt(F1 / g) - (F1 / g) * m.sin(10.0 * m.pi * F1))

	exp.Response("F1")["Value"] = F1
	exp.Response("F2")["Value"] = F2

	success = True

	for s in exp.SuccessFlags:
		s["Success"] = success

