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

