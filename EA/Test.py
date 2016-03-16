#    duh, a heuristics-based design exploration code.
#    Copyright (C) 2016 Hiromasa Kato <hiromasa at gmail.com>
#
#    This file is part of duh.
#
#    duh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    duh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

