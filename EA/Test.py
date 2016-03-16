import TestCases
from ResponseEvaluator import *
from PenaltyEvaluator import *
from FitnessEvaluator import *

from Population import *

from MonoObjectiveGA import *
from MonoObjectiveSurrogateGA import *

def Main():

	f = TestCases.Rosenbrock()
	ch = f.Chromosome()

	resEval = ResponseEvaluator(f)

	penEval = PenaltyEvaluator()
	penEval.ObjectivePenalties = f.Objectives()
	penEval.ConstraintPenalties = f.Constraints()

	fitnessEval = FitnessEvaluator()

	if False:
		opti = MonoObjectiveGA(ch, resEval, penEval, fitnessEval, 400, 2)
	else:
		pop = Population()
		for i in range(4):
			pop.append(ch.Clone())
		pop.Randomize()
		resEval.Evaluate(pop)
		penEval.Evaluate(pop)
		fitnessEval.Evaluate(pop)
		pop.SortByFitness()

		opti = MonoObjectiveSurrogateGA(ch, resEval, penEval, fitnessEval, pop)

	opti.Start(50)

if __name__ == "__main__":
	Main()

