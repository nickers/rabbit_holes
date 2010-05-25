# -*- coding: utf-8 -*-
from twisted.web import resource, server
from twisted.internet import reactor, defer
from charades.ajax_queue import *
from charades.game_state import game_state


class Game(resource.Resource):
	
	isLeaf = False
	
	def __init__(self):
		print "Init game"
		self.games = {}

	def render(self, request):
		""" Handle GET request, but don't finish it """
		game_id = ""
		print str(request.postpath)
		
		if len(request.postpath)>=1:
			game_id = unicode(request.postpath[0])
		
		print "Game id: ", game_id
		
		if not self.games.has_key(game_id):
			self.games[game_id] = ajax_queue()
		
		q = self.games[game_id]
		q.add_listener(request)
		
		
		if len(request.postpath)>=2 and request.postpath[1]=="post":
			q = self.games[game_id]
			q.add_message("test")
		
		return server.NOT_DONE_YET


class GameCommandsWait(resource.Resource):
	""" Zawieś się w oczekiwaniu na komendy """
	
	isLeaf = True
	
	def __init__(self):
		self.games = registry.getComponent(game_state)
		if not self.games:
			self.games = {}
			registry.setComponent(game_state, self.games)

	def render(self, request):
		""" Handle GET request, but don't finish it """
		game_id = ""
		
		if len(request.postpath)==1:
			game_id = unicode(request.postpath[0])
			print "Game id: ", game_id
			
			if not self.games.has_key(game_id):
				self.games[game_id] = ajax_queue()
			
			q = self.games[game_id]
			q.add_listener(request)
		
		return server.NOT_DONE_YET
