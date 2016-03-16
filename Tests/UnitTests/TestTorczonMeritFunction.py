# $Id: TestTorczonMeritFunction.py 87 2011-02-17 16:46:52Z kato $

import EA

def Main():

	case = EA.TestCases.Rosenbrock()

	chromosome = case.Chromosome()
	chromosome.Responses.append(EA.Value("TorczonMerit", "FLOAT"))

	resEval = EA.ResponseEvaluator(case)
	penaltyEval = EA.PenaltyEvaluator()
	penaltyEval.ObjectivePenalties = case.Objectives()
	penaltyEval.ConstraintPenalties = case.Constraints()

	fitnessEval = EA.FitnessEvaluator()

	print chromosome

	pop = EA.Population()
	for i in range(10):
		pop.append(chromosome.Clone())
	pop.Randomize()

	resEval.Evaluate(pop)
	penaltyEval.Evaluate(pop)
	fitnessEval.Evaluate(pop)

	torczon = EA.TorczonMeritFunction(pop, chromosome, 1.0, "TorczonMerit")
	torczon.Evaluate(pop)

	print pop

	#pop.SortByFitness()

	#print pop

if __name__ == "__main__":
	Main()
