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
# $Id: ExperimentPlan.py 130 2013-10-29 01:15:50Z kato $

from Experiment import Experiment

class ExperimentPlan(list):

	def __init__(self, chain):
		self.Chain = chain

	def __getitem__(self, key):

		if isinstance(key, slice):
			newPlan = ExperimentPlan(self.Chain)
			for i in range(*key.indices(len(self))):
				newPlan.append(self[i])
			return newPlan
		elif isinstance(key, int):
			return list.__getitem__(self, key)
		else:
			return IndexError

	def __getslice__(self, i, j):

		return self.__getitem__(slice(i, j))

	def FindByID(self, expID):
		match = filter(lambda e: e.ID == expID, self)
		assert(len(match) == 1)
		return match[0]

	def NextReadyExperiment(self):
		for e in self:
			if e.Status == "READY":
				return e

	def Export(self, o):

		print >>o, "# Version 1.0 Experiment Plan"
		print >>o, "# Parameters"
		buf = ""
		for p in self.Chain.Parameters:
			buf += "%s\t" % p["Name"]
		print >>o, buf
		print >>o, "# Responses"
		buf = ""
		for r in self.Chain.Responses:
			buf += "%s\t" % r["Name"]
		print >>o, buf
		print >>o, "# Success Flags"
		buf = ""
		for s in self.Chain.SuccessFlags:
			buf += "%s\t" % s["Name"]
		print >>o, buf
		print >>o, "# ExpID, Status, [Parameters], [Responses], [Success Flags]"
		for e in self:
			buf = ""
			buf += "%d\t" % e.ID
			buf += "%s\t" % e.Status
			for p in e.Parameters:
				buf += "%20.12e\t" % p["Value"]
			for r in e.Responses:
				buf += "%20.12e\t" % r["Value"]
			for s in e.SuccessFlags:
				buf += "%d\t" % s["Success"]
			print >>o, buf

	def Import(self, o):

		line = o.readline().strip()
		if line != "# Version 1.0 Experiment Plan":
			print "Unknown plan file format"
			raise IOError

		o.readline()
		line = o.readline()
		paramNames = line.split()
		if len(paramNames) != len(self.Chain.Parameters):
			print "Wrong number of parameters"
			raise IOError
		numParams = len(paramNames)

		o.readline()
		line = o.readline()
		respNames = line.split()
		if len(respNames) != len(self.Chain.Responses):
			print "Wrong number of responses"
			raise IOError
		numResps = len(respNames)

		o.readline()
		line = o.readline()
		successNames = line.split()
		if len(successNames) != len(self.Chain.SuccessFlags):
			print "Wrong number of success flags"
			raise IOError
		numSuccesses = len(successNames)

		o.readline()
		for line in o:
			tokens = line.split()
			expID = int(tokens[0])
			status = tokens[1]
			paramValues = map(float, tokens[2:2 + numParams])
			respValues = map(float, tokens[2 + numParams:2 + numParams + numResps])
			successValues = map(int, tokens[2 + numParams + numResps:2 + numParams + numResps + numSuccesses])

			exp = Experiment(expID, self.Chain)
			exp.Status = status
			for i, v in enumerate(paramValues):
				name = paramNames[i]
				exp.Parameter(name)["Value"] = v
			for i, v in enumerate(respValues):
				name = respNames[i]
				exp.Response(name)["Value"] = v
			for i, v in enumerate(successValues):
				name = successNames[i]
				assert(v == 0 or v == 1)
				exp.SuccessFlag(name)["Success"] = v == 1

			self.append(exp)

	def NextAvailableID(self):

		if len(self) == 0:
			nextID = 1
		else:
			sortedExps = sorted(self, lambda e1, e2: cmp(e1.ID, e2.ID))
			lastID = sortedExps[-1].ID
			nextID = lastID + 1
		return nextID

if __name__ == "__main__":
	Test()

