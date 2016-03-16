import Backbone

def Rosenbrock2D(exp):

	x1 = exp.Parameter("X1")["Value"]
	x2 = exp.Parameter("X2")["Value"]

	f = pow(1.0 - x1, 2) + 100.0 * pow(x2 - x1 * x1, 2)

	exp.Response("F1")["Value"] = f

	success = x1 + x2 <= 1.0
	success = True

	for s in exp.SuccessFlags:
		s["Success"] = success

