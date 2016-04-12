# $Id: WeldedBeam.py 111 2012-06-13 14:57:15Z kato $

import Backbone
import math as m

def WeldedBeam(exp):

	b = exp.Parameter("b")["Value"]
	t = exp.Parameter("t")["Value"]
	l = exp.Parameter("l")["Value"]
	h = exp.Parameter("h")["Value"]

	cost = 1.10471 * h * h * l + 0.04811 * t * b * (14.0 + l)

	tau1 = 6000.0 / (m.sqrt(2.0) * h * l)
	lsq = l * l
	A = (h + t) * (h + t)
	B = m.sqrt(0.25 * (lsq + A))
	tau2 = 6000.0 * (14.0 + 0.5 * l) * B / (2.0 * 0.707 * h * l * (lsq / 12.0 + 0.25 * A))
	tau = m.sqrt(tau1 * tau1 + tau2 * tau2 + l * tau1 * tau2 / B)
	sigma = 504000.0 / (t * t * b)
	Pc = 64746.022 * (1.0 - 0.0282346 * t) * t * b * b * b

	# Constraints
	g1 = 13600.0 - tau		# >= 0
	g2 = 30000.0 - sigma	# >= 0
	g3 = Pc - 6000.0		# >= 0
	g4 = b - h				# >= 0
	g5 = 2.1952 / (t * t * t * b)	# = delta <= 0.25

	exp.Response("Cost")["Value"] = cost
	exp.Response("G1")["Value"] = g1
	exp.Response("G2")["Value"] = g2
	exp.Response("G3")["Value"] = g3
	exp.Response("G4")["Value"] = g4
	exp.Response("G5")["Value"] = g5

	for s in exp.SuccessFlags:
		s["Success"] = True

