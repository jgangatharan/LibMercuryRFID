#!/usr/bin/env python

import sys
import ctypes
import time
import threading
import Queue

lib = ""
communicatorQueue = ""
callbackList = ""
comThread = ""
callbackHandler = ""

class Communicator(threading.Thread):

	def __init__(self, messageQueue):
		super(Communicator, self).__init__()
		self.messageQueue = messageQueue

	def run(self):
		while True:
			try:
				msg = self.messageQueue.get(True)
				if msg == "exit":
					break
				else:
					
					#msg = "Reader: " + taginfo[0] + " TAG: " + taginfo[1] + " RSSI: " + taginfo[2] + "dB Phase: " + taginfo[3] + u"\u00B0 Frequency: " + taginfo[4] + " Timestamp (high): " + taginfo[5] + " Timestamp (low): " + taginfo[6]
					pass
					#digest message, send to designated callback func
			except:
				print("Unexpected error: ", sys.exc_info()[0])

class CallbackHandler(object):

	def __init__(self, messageQueue):
		super(CallbackHandler, self).__init__()
		self.messageQueue = messageQueue
		self.callback = ctypes.CFUNCTYPE(ctypes.c_byte, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))(self.callbackHandler)

	def callbackHandler(self, char_ptr_ptr):
		taginfo = []

		for i in xrange(0, 7):
			taginfo.append("")
			for j in char_ptr_ptr[i]:
				if j == "\0":
					break
				else:
					taginfo[i] += j

		self.messageQueue.put(taginfo)

		return 0

def init():

	global communicatorQueue, comThread, lib, callbackHandler, callbackList

	communicatorQueue = Queue.Queue()
	comThread = Communicator(communicatorQueue)
	comThread.start()

	lib = ctypes.CDLL("libmerc/rfid.so")

	callbackHandler = CallbackHandler(communicatorQueue)

	callbackList = {}

def startReader(deviceURI, callbackFunction):

	global lib, callbackList, callbackHandler

	readerID = lib.startReader(deviceURI, callbackHandler.callback)

	callbackList[readerID] = callbackFunction
	print readerID
	return readerID

def stopReader(readerID):

	global lib

	lib.stopReader(readerID)

def close():

	global communicatorQueue, lib, callbackList

	communicatorQueue.put("exit")
	lib.closeRFID()
	callbackList = {}