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

from Population import *

from SPEA2 import *
from ParetoSurrogateGA import ParetoSurrogateGA

def DumpObjectives(f, pop):

	for indi in pop:
		o = indi.Objectives
		print >>f, o[0], o[1]

def Main():

	#f = TestCases.ZDT1()
	#f = TestCases.ZDT2()
	f = TestCases.ZDT3()
	ch = f.Chromosome()

	resEval = ResponseEvaluator(f)

	penEval = PenaltyEvaluator()
	penEval.ObjectivePenalties = f.Objectives()
	penEval.ConstraintPenalties = f.Constraints()

	opti = SPEA2(ch, resEval, penEval, 100, 20)

	opti.Start(50)

	DumpObjectives(open("pop.dat", "w"), opti.Population)
	DumpObjectives(open("archive.dat", "w"), opti.Archive)

def MainSurrogate(maxloop = 50, truncation = "OBJECTIVE"):

	NDOE = 10
	NUPDATE = 3

	f = TestCases.ZDT3()
	ch = f.Chromosome()

	resEval = ResponseEvaluator(f)

	penEval = PenaltyEvaluator()
	penEval.ObjectivePenalties = f.Objectives()
	penEval.ConstraintPenalties = f.Constraints()

	pop = Population()
	for i in range(NDOE):
		indi = ch.Clone()
		indi.Randomize()
		pop.append(indi)

	resEval.Evaluate(pop)
	penEval.Evaluate(pop)

	opti = ParetoSurrogateGA(ch, resEval, penEval, pop, NUPDATE, truncation)
	opti.Start(maxloop)

	print pop
	DumpObjectives(open("pop.dat", "w"), pop)

if __name__ == "__main__":
	import sys
	MainSurrogate(int(sys.argv[1]), sys.argv[2])

