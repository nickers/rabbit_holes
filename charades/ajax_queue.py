# -*- coding: utf-8 -*-
from twisted.web import resource, server
from twisted.internet import reactor, defer
import threading, simplejson as json
import game_file

class ajax_queue:
	
	def __init__(self):
		self.data = []
		self.listeners = []
		self.data_lock = threading.Lock()
		self.listeners_lock = threading.Lock()
		self.notify_lock = threading.Lock()
	
	def add_message(self, message):
		""" Dodaj wiadomosc do listy na stale """
		self.data_lock.acquire()
		self.data.append(message)
		self.data_lock.release()
		self.__notify()
		return None
	
	#def send_message(self, message):
	#	""" ??
	#	Wyslij wiadomosc do kolejki, ale nie zapisuj w historii """
	#	return None
	
	def add_listener(self, listener, next_message=0):
		self.listeners_lock.acquire()
		part = self.data[next_message:]
		if (len(part)==0):
			self.listeners.append((listener, next_message))
		else:
			self.__send_part(listener, next_message)
		self.listeners_lock.release()
		return True
	
	def __notify(self):
		self.listeners_lock.acquire()
		sendto = self.listeners
		self.listeners = []
		self.listeners_lock.release()
		
		#self.notify_lock.acquire()
		for (dest, next_message) in sendto:
			self.__send_part(dest, next_message)
			
		#self.notify_lock.release()
		return None
	
	def __send_part(self, dest, next_message):
		print dest, " == ", next_message
		try:
			part = self.data[next_message:]
			encoded = json.dumps(part)
			dest.write(encoded)
			dest.finish()
			print "process: %s" %(encoded,)
		except:
			print "Error while sending data"
	