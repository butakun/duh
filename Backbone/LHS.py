# $Id: LHS.py 127 2013-05-17 16:35:24Z kato $

import numpy as n
import random

def LHS(sampleCount, dimension):

	pp = n.zeros((sampleCount, dimension))
	for d in range(dimension):
		p = n.linspace(0.0, 1.0, sampleCount)
		random.shuffle(p)
		#for i in range(sampleCount, 1, -1):
		#	j = random.randrange(i)
		#	p[j], p[i - 1] = p[i - 1], p[j]
		pp[:, d] = p
	return pp

