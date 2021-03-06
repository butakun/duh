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
# $Id: Dispatcher.py 44 2010-09-21 15:31:56Z kato $

import Runner
import os

class Dispatcher(object):
	"""
	Dispatcher maintains a list of listener objects (listeners).
	A listener must implement MessageReceived method, which will be invoked by
	the dispatcher when the status of a job changes, like when it's finished.
	"""

	def __init__(self, runner = None, listeners = None):

		if not runner:
			runner = Runner.DefaultRunner()
		self.Runner = runner
		self.Listeners = []
		if listeners:
			self.Listeners.extend(listeners)

	def Submit(self, job):

		raise Error

	def Quit(self):

		raise Error

	def IsFull(self):

		raise Error

	def JobFinished(self, job):

		pass

