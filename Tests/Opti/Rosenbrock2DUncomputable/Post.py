import EA, Surrogate

import pickle
import numpy as n

def Main(f):

	a = pickle.load(f)

	resModel = a["ResponseSurrogate"]
	sucModel = a["SuccessSurrogate"]
	trustRegion = a["TrustRegion"]

