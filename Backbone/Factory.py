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
# $Id: Factory.py 96 2011-04-28 03:49:06Z kato $

import EA
from Experiment import Experiment

def Chromosome(chain):

	indi = EA.Individual()
	for param in chain.Parameters:
		name = param["Name"]
		valueType = param["Type"]
		minValue = param["Min"]
		maxValue = param["Max"]
		refValue = param["Ref"]
		p = EA.BoundedValue(name, valueType, refValue, refValue, minValue, maxValue)
		indi.DesignParameters.append(p)

	for resp in chain.Responses:
		name = resp["Name"]
		valueType = resp["Type"]
		r = EA.Value(name, valueType, 0.0)
		indi.Responses.append(r)

	return indi

def ExperimentFromIndividual(chain, indi):

	exp = Experiment(-1, chain)

	for p in indi.DesignParameters:
		param = exp.Parameter(p.Name)
		param["Value"] = p.Value

	return exp

def IndividualFromExperiment(chromosome, exp):

	indi = chromosome.Clone()
	indi.ID = exp.ID
	for p in indi.DesignParameters:
		value = exp.Parameter(p.Name)["Value"]
		p.Value = value
	for r in indi.Responses:
		value = exp.Response(r.Name)["Value"]
		r.Value = value
	indi.Success = exp.IsSuccess()
	return indi

def PopulationFromPlan(chromosome, plan):

	pop = EA.Population()
	for exp in plan:
		pop.append(IndividualFromExperiment(chromosome, exp))
	return pop

def CreatePenaltyEvaluator(config):

	penEval = EA.PenaltyEvaluator()

	objectiveSpecs = config["Objectives"]
	for spec in objectiveSpecs:
		name = spec["Name"]
		penaltyType = spec["Type"]
		weight = spec["Weight"]
		ref = spec["Reference"]
		exponent = spec["Exponent"]
		penalty = EA.Penalty(penaltyType, name, weight, ref, exponent = exponent)
		penEval.ObjectivePenalties.append(penalty)

	if not config.has_key("Constraints"):
		return penEval

	constraintSpecs = config["Constraints"]
	for spec in constraintSpecs:
		name = spec["Name"]
		penaltyType = spec["Type"]
		weight = spec["Weight"]
		ref = spec["Reference"]
		imposed = spec["Imposed"]
		exponent = spec["Exponent"]
		penalty = EA.Penalty(penaltyType, name, weight, ref, imposed = imposed, exponent = exponent)
		penEval.ConstraintPenalties.append(penalty)

	return penEval

