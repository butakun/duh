# $Id: Utils.py 84 2011-02-08 02:25:48Z kato $

from Database import Database
import numpy as n

def ResponseDatabaseFromPlan(plan, return_ids = False):

	ids = []
	db = Database()
	for exp in plan:
		if not exp.IsSuccess():
			continue
		params = exp.ParametersAsVector()
		responses = exp.ResponsesAsVector()
		db.append([params, responses])
		ids.append(exp.ID)
	if return_ids:
		return db, ids
	else:
		return db

def ResponseDatabaseFromPopulation(pop):

	db = Database()
	for indi in pop:
		if not indi.Success:
			continue
		params = indi.DesignParameters.AsVector()
		responses = indi.Responses.AsVector()
		db.append([params, responses])
	return db

def SuccessDatabaseFromPopulation(pop):

	db = Database()
	for indi in pop:
		params = indi.DesignParameters.AsVector()
		responses = n.array([float(indi.Success)])
		db.append([params, responses])
	return db

