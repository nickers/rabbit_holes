# -*- coding: utf-8 -*-
from twisted.web import resource, server, util
from twisted.web.static import Registry
from twisted.internet import reactor, defer
import simplejson as json
from jinja2 import Template, Environment, PackageLoader
from commands import process_message, send_map_command
from charades.ajax_queue import *
from charades.game_state import game_state, FT
from helpers import ensure_game_exists

def get_game_by_id(game_id):
	return None

class Game(resource.Resource):
	
	isLeaf = True
	
	def __init__(self):
		print "Init game"

	def render(self, request):
		username = request.getCookie('username')

		game_id = ""
		try:
			if len(request.postpath)>=1:
				game_id = unicode(request.postpath[0])
		except:
			game_id = ""
		
		if username.strip()=="":
			request.redirect('/login/')
#			request.finish()
			return ""
		
		if game_id.strip()=="" or not game_state.exists(game_id):
			request.redirect('/list_games/')
#			request.finish()
			return ""
		
		game = game_state.get(game_id)
		color = -1
		for k in game.players.iterkeys():
			if game.players[k]==username:
				color = k
		
		### game_id, player_name, player_color
		tpl_env = Environment(loader=PackageLoader('charades','templates'))
		tpl = tpl_env.get_template("say.html")
		return unicode(tpl.render({'game_id':game_id, 'player_name':username, 'player_color':color})).encode('utf-8')


class GameCommandsWait(resource.Resource):
	""" Zawieś się w oczekiwaniu na komendy """
	
	isLeaf = True

	def render(self, request):
		""" Handle GET request, but don't finish it """
		game_id = ""
		
		if len(request.postpath)==2:
			game_id = unicode(request.postpath[0])
			next_id = int(request.postpath[1])

			if not game_state.exists(game_id):
				return "GAME NOT EXISTS";
			
			game = game_state.get(game_id)
			game.queue.add_listener(request, next_id)
		
			return server.NOT_DONE_YET
		return "BAD ARGUMENTS NUMBER"


class GameCommandProcess(resource.Resource):
	
	isLeaf = True
	
	def render(self, request):
		game_id = unicode(request.postpath[0])
		
		if not game_state.exists(game_id):
			return "GAME NOT EXISTS";
		
		request.content.seek(0, 0)
		command = request.content.read()
		command = json.loads(command)

		game = game_state.get(game_id)
		process_message(game, command)
		
		return "OK"


class LoginProcess(resource.Resource):
	isLeaf = True
	
	def render(self, request):
		print "login"
		if 'username' in request.args and request.args['username'][0].strip()!='':
			username = request.args['username'][0]
			request.addCookie('username', username)
			request.redirect('list_games')
		else:
			request.redirect('/enter_name.html')
		return ""


class ListGamesProcess(resource.Resource):
	isLeaf = True
	
	def render(self, request):
		print "list games"
		username = request.getCookie('username')
		tpl_env = Environment(loader=PackageLoader('charades','templates'))
		tpl = tpl_env.get_template("list_games.html")
		list = game_state.list()
		games = []
		for id in list:
			game = game_state.get(id)
			if not game.finished:
				game_dest = {
					'id' : game.id,
					'white' : game.players[FT.WHITE],
					'black' : game.players[FT.BLACK]
				}
				games.append(game_dest)
		return unicode(tpl.render({'games':games, 'username':username})).encode('utf-8')
		

class CreateGameProcess(resource.Resource):
	isLeaf = True
	
	def render(self, request):
		username = request.getCookie('username')
		game_id = ensure_game_exists(username)
		request.redirect('/game/' + game_id)
#		request.finish()
		return ""

class EnterGameProcess(resource.Resource):
	isLeaf = True
	
	def render(self, request):
		username = request.getCookie('username')
		game_id = unicode(request.postpath[0])
		game_id = ensure_game_exists(username, game_id)
		game = game_state.get(game_id)
		game.players[FT.BLACK] = username
		request.redirect('/game/' + unicode(game_id).encode('utf-8'))
#		request.finish()
		return str(u'/game/%s'%game_id)
