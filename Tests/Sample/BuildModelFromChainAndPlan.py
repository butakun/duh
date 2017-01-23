import Backbone, Surrogate
import numpy as np

def Main(chainfilename, planfilename):

	# Read chain
	chain = Backbone.Mothership.LoadChain(chainfilename)

	# Make an empty plan based on the chain
	plan = Backbone.ExperimentPlan(chain)
	# Then populate the empty plan
	plan.Import(open(planfilename))

	# Build database of training samples
	db, ids = Surrogate.Utils.ResponseDatabaseFromPlan(plan, return_ids = True)

	# Construct RBFN and train with the database
	rbfn = Surrogate.RBFNetwork()
	rbfn.Train(db)

	# Make a parameter vector. We can tell the number of parameters from the chain.
	# Note that I'm using numpy.random. x is *not* guaranteed to be within the parameter range.
	x = np.random.random(len(chain.Parameters))

	# Now evaluate the model with the x.
	f = rbfn.Evaluate(x)

	print "Input = ", x
	print "Response = ", f

if __name__ == "__main__":
	import sys
	Main(sys.argv[1], sys.argv[2])

