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

