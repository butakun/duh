#!/usr/bin/env python

import math as m
import sys, time

def Main(i):

	F = open("Parameters.in")
	x1 = float(F.readline().split()[0])
	x2 = float(F.readline().split()[0])
	del F

	f = m.pow(1.0 - x1, 2) + 100.0 * m.pow(x2 - x1 * x1, 2) + float(i)

	time.sleep(5)

	print >>open("Responses%d.out" % i, "w"), f
	print >>open("Success%d.out" % i, "w"), "success"

if __name__ == "__main__":
	Main(int(sys.argv[1]))

