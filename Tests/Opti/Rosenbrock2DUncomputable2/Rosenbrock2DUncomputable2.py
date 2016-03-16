#!/usr/bin/env python

import math as m

def Main():

	F = open("Parameters.in")
	x1 = float(F.readline().split()[0])
	x2 = float(F.readline().split()[0])
	del F

	f = m.pow(1.0 - x1, 2) + 100.0 * m.pow(x2 - x1 * x1, 2)

	print >>open("Responses.out", "w"), f

	d = x1 + x2
	if d < 1.0:
		residual = 1e-5
	else:
		residual = 0.1
	print >>open("Residual.out", "w"), residual

if __name__ == "__main__":
	Main()

