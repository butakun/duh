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
# $Id: Looper.py 63 2010-11-11 16:17:12Z kato $

import threading, Queue

class Looper(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self._MessageQueue = Queue.Queue()
		self._QuitEvent = threading.Event()

	def run(self):

		try:
			while not self._QuitEvent.is_set():
				#print "Looper: waiting for msg"
				try:
					msg = self._MessageQueue.get(True, 1)
				except Queue.Empty:
					continue
				self.MessageReceived(msg)
		except:
			print "LooperError caught"
			raise

	def Start(self):
		self.start()

	def MessageReceived(self, msg):
		if msg["what"] == "QUIT":
			#print "Looper: QUIT message received"
			self.QuitRequested()
			self._QuitEvent.set()

	def PostMessage(self, msg):
		self._MessageQueue.put(msg)

	def PostQuit(self):
		self.PostMessage({"what":"QUIT"})

	def QuitRequested(self):
		print "Looper: QuitRequested"

class TestLooper(Looper):
	def MessageReceived(self, msg):
		Looper.MessageReceived(self, msg)
		if msg["what"] == "TEST":
			print msg["message"]

def Test():
	import time

	looper = TestLooper()
	looper.Start()

	for i in range(10):
		looper.PostMessage({"what":"TEST", "message":"test %d" % i})
		time.sleep(2)

	looper.PostQuit()

if __name__ == "__main__":
	Test()

