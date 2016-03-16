# $Id: Rastrigin2D.py 133 2014-02-18 02:33:09Z kato $

import Backbone
import numpy as np

def Rastrigin2D(exp):

	X = exp.ParametersAsVector()

	n = 2
	A = 10
	f = A * n + np.sum(X * X - A * np.cos(2.0 * np.pi * X))

	exp.Response("F1")["Value"] = f

	success = True

	for s in exp.SuccessFlags:
		s["Success"] = success

