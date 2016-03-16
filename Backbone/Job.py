# $Id: Job.py 44 2010-09-21 15:31:56Z kato $

class Job(object):

	def __init__(self, expID, commandID, command, preHooks = None, postHooks = None, runner = None):

		self.ExpID = expID
		self.CommandID = commandID
		self.Command = command
		self.PostHooks = preHooks
		self.PreHooks = preHooks
		self.Runner = runner

