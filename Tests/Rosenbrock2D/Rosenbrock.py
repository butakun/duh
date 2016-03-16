# $Id: Rosenbrock.py 22 2010-06-09 05:52:13Z kato $

import os

def Main(dim):

	lines = open("Parameters.in").read().split(os.linesep)
	X = [0] * dim
	for d in range(dim):
		X[d] = float(lines[d].split()[0])

	F = (1.0 - X[0]) * (1.0 - X[0]) + 100.0 * (X[1] - X[0] * X[0]) * (X[1] - X[0] * X[0])

	open("Responses.out", "w").write("%20.12e\n" % F)
	open("Success.out", "w").write("success\n")

if __name__ == "__main__":
	Main(2)

