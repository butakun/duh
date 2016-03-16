# $Id: SequentialDispatcher.py 44 2010-09-21 15:31:56Z kato $

from Dispatcher import Dispatcher
import os

class SequentialDispatcher(object):

	def __init__(self):

		Dispatcher.__init__(self)

	def Submit(self, job):


