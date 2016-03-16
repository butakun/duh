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
# $Id: Job.py 44 2010-09-21 15:31:56Z kato $

class Job(object):

	def __init__(self, expID, commandID, command, preHooks = None, postHooks = None, runner = None):

		self.ExpID = expID
		self.CommandID = commandID
		self.Command = command
		self.PostHooks = preHooks
		self.PreHooks = preHooks
		self.Runner = runner

