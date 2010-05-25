# -*- coding: utf-8 -*-
from twisted.web import resource, server
from twisted.web.static import Registry
from twisted.internet import reactor, defer
import simplejson as json
from charades.ajax_queue import *
from charades.game_state import game_state

def get_game_by_id(game_id):
	return None

class Game(resource.Resource):
	
	isLeaf = True
	
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

	def render(self, request):
		""" Handle GET request, but don't finish it """
		game_id = ""
		
		if len(request.postpath)==2:
			game_id = unicode(request.postpath[0])
			next_id = int(request.postpath[1])
			
			game = game_state.get(game_id)
			game.queue.add_listener(request, next_id)
		
			return server.NOT_DONE_YET
		return "BAD ARGUMENTS NUMBER"


class GameCommandProcess(resource.Resource):
	
	isLeaf = True
	
	def render(self, request):
		game_id = unicode(request.postpath[0])
		
		request.content.seek(0, 0)
		command = request.content.read()
		command = json.loads(command)
		
		game = game_state.get(game_id)
		game.queue.add_message(command);
		
		return "OK"

