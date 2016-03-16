# $Id: TestDebConstraintFitness.py 87 2011-02-17 16:46:52Z kato $

import EA

def Main():

	case = EA.TestCases.RosenbrockUncomputable()

	resEval = EA.ResponseEvaluator(case)
	penaltyEval = EA.PenaltyEvaluator()
	penaltyEval.ObjectivePenalties = case.Objectives()
	penaltyEval.ConstraintPenalties = case.Constraints()

	fitnessEval = EA.FitnessEvaluator()


	pop = EA.Population()
	for i in range(10):
		pop.append(case.Chromosome())

	pop.Randomize()
	resEval.Evaluate(pop)
	penaltyEval.Evaluate(pop)

	print pop

	fitnessEval.Evaluate(pop)

	pop.SortByFitness()

	print pop

if __name__ == "__main__":
	Main()
