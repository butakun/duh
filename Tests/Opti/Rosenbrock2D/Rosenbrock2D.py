#!/usr/bin/env python

import math as m

def Main():

	F = open("Parameters.in")
	x1 = float(F.readline().split()[0])
	x2 = float(F.readline().split()[0])
	del F

	f = m.pow(1.0 - x1, 2) + 100.0 * m.pow(x2 - x1 * x1, 2)

	print >>open("Responses.out", "w"), f
	print >>open("Success.out", "w"), "success"

if __name__ == "__main__":
	Main()

