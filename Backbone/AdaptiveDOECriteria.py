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
# $Id: AdaptiveDOECriteria.py 135 2014-07-29 07:39:17Z kato $

import numpy as np
import Surrogate
from Backbone import *

def SimpleLOO(plan):

	F, FLOO = [], []
	errors = []
	for iloo, expLOO in enumerate(plan):

		planLOO = ExperimentPlan(plan.Chain)
		for i, exp in enumerate(plan):
			if i != iloo:
				planLOO.append(exp)
		db = Surrogate.Utils.ResponseDatabaseFromPlan(planLOO)
		surrogate = Surrogate.RBFNetwork()
		surrogate.Train(db)

		xLOO = expLOO.ParametersAsVector()
		fLOO = surrogate.Evaluate(xLOO)
		f = expLOO.ResponsesAsVector()

		error = f - fLOO
		errors.append(error)

		F.append(f)
		FLOO.append(fLOO)

	errors = np.array(errors)
	emin = errors.min(axis=0)
	emax = errors.max(axis=0)
	errorsScaled = (errors - emin) / (emax - emin)

	print errors
	print errorsScaled

	for i, exp in enumerate(plan):
		exp["Error"] = errorsScaled[i].sum()

	F = np.array(F)
	FLOO = np.array(FLOO)

	print "*** Leave-One-Out correlation coefficients ***"
	for iresp in range(F.shape[1]):
		r = np.corrcoef(F[:, iresp], FLOO[:, iresp])[0, 1]
		print "  R = %f\t# for %s" % (r, plan.Chain.Responses[iresp]["Name"])

