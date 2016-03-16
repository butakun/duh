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

