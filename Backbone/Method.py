# $Id: Method.py 44 2010-09-21 15:31:56Z kato $

import threading

class Method(object):

	def __init__(self):
		self._Lock = threading.Lock()

	def Lock(self):
		self._Lock.acquire()

	def Unlock(self):
		self._Lock.release()

	def IsDone(self):
		raise Error

