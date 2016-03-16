# $Id$

import threading

Lock = None

Level = 100

def Disable():
	global Level
	Level = -1

def Init():
	global Lock
	Lock = threading.Lock()

def Out(buf):
	if Level < 0:
		return

	global Lock
	if not Lock:
		Init()

	Lock.acquire()
	print buf
	Lock.release()

