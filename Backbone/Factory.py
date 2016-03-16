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
		penalty = EA.Penalty(penaltyType, name, weight)
		penEval.ObjectivePenalties.append(penalty)

	if not config.has_key("Constraints"):
		return penEval

	constraintSpecs = config["Constraints"]
	for spec in constraintSpecs:
		name = spec["Name"]
		penaltyType = spec["Type"]
		weight = spec["Weight"]
		imposed = spec["Imposed"]
		penalty = EA.Penalty(penaltyType, name, weight, imposed = imposed)
		penEval.ConstraintPenalties.append(penalty)

	return penEval

