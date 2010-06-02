# -*- coding: utf-8 -*-
from charades.game_state import game_state, FT

class user_command:
	def __init__(self):
		self.action = ""
		self.user = ""

class say_command(user_command):
	
	class say_to_all(user_command):
		def __init__(self, msg):
			self.action = 'say'
			self.user = msg['user']
			self.msg = msg['msg']
		def process(self, game):
			pass
	
	def validate(self, game, msg):
		""" sprawdz czy ruch jest prawidlowy """
		print 'Say: ', msg['msg']
		return True
	
	def process(self, game, msg):
		return [say_command.say_to_all(msg)]

class move_command(user_command):
	
	class add_rabbit(user_command):
		def __init__(self, who, x, y, c):
			self.action = 'set_rabbit'
			self.user = who
			self.x = x
			self.y = y
			self.color = c
		
		def process(self, game):
			game.rabbits[self.x][self.y] = self.color
	
	class del_rabbit(user_command):
		def __init__(self, who, x, y):
			self.action = 'set_rabbit'
			self.user = who
			self.x = x
			self.y = y
			self.color = FT.EMPTY
		
		def process(self, game):
			game.rabbits[self.x][self.y] = self.color
	
	class set_round(user_command):
		def __init__(self, c):
			self.action = 'set_round'
			self.user = ''
			self.color = c
		def process(self, game):
			if game.is_player_blocked(game.round[0]):
				game.change_round()
	
	class set_score(user_command):
		def __init__(self, game):
			self.action = 'set_score'
			self.user = '';
			self.black = 0
			self.white = 0
		
		def process(self, game):
			self.black = game.get_player_score(FT.BLACK)
			self.white = game.get_player_score(FT.WHITE)
			
	
	def process(self, game, msg):
		import math
		dx = (int)(math.fabs(msg['srcX']-msg['dstX']))
		dy = (int)(math.fabs(msg['srcY']-msg['dstY']))
		who = game.players[game.round[0]]
		col = game.round[0]
		
		game.change_round()
		
		if (dx>=2 or dy>=2):
			return [move_command.add_rabbit(who, msg['dstX'], msg['dstY'], col),
					move_command.set_score(game),
					move_command.set_round(game.round[0])]
		else:
			return [move_command.del_rabbit(who, msg['srcX'], msg['srcY']),
					move_command.add_rabbit(who, msg['dstX'], msg['dstY'], col),
					move_command.set_score(game),
					move_command.set_round(game.round[0])]
		
	def validate(self, game, msg):
		
		return game.is_valid_move(msg['srcX'], msg['srcY'], msg['dstX'], msg['dstY'])
		
		import math
		
		round = game.round[0]
		valid = True

		try:
			srcColor = game.rabbits[msg['srcX']][msg['srcY']]
			dstColor = game.rabbits[msg['dstX']][msg['dstY']]
			
			srcMap = game.map[msg['srcX']][msg['srcY']]
			dstMap = game.map[msg['dstX']][msg['dstY']]
			
			# from my colour to empty
			if srcColor!=round:
				valid = False
			if dstColor!=FT.EMPTY:
				valid = False
				
			# can't move from hole or any NON empty field
			if srcMap!=FT.EMPTY:
				valid = False
			
			# must move to empty or hole
			if dstMap!=FT.EMPTY and dstMap!=FT.HOLE:
				valid = False
			
			# move has valid vector
			dx = (int)(math.fabs(msg['srcX']-msg['dstX']))
			dy = (int)(math.fabs(msg['srcY']-msg['dstY']))
			validMoves = [(0,0),(1,0),(0,1),(1,1),(2,0),(0,2),(2,2)]
			try:
				validMoves.index((dx,dy))
			except: # invalid move
				valid = False
			
			# if jump then must jump over own color
			if dx==2 or dy==2:
				over = game.rabbits[int((msg['srcX']+msg['dstX'])/2)][int((msg['srcY']+msg['dstY'])/2)]
				if over!=round:
					valid = False
			
		except: # mus be invalid position
			print " => Exception"
			valid = False
		
#		for y in range(6):
#			for x in range(6):
#				print game.rabbits[x][y], " ",
#			print ""
		
		return valid
		
# ---------------
class send_map_command(user_command):
	class set_rabbit(user_command):
		def __init__(self, who, x, y, c):
			self.action = 'set_rabbit'
			self.user = who
			self.x = x
			self.y = y
			self.color = c
		def process(self, game):
			pass
			
	class set_map(user_command):
		def __init__(self, who, x, y, c):
			self.action = 'set_map'
			self.user = who
			self.x = x
			self.y = y
			self.color = c
		def process(self, game):
			pass
	
	def __init__(self, user=None):
		self.action = 'send_map'
		self.user = user
	
	def validate(self, game, msg):
		return True
	
	def process(self, game, msg):
		who = msg['user']
		dim = len(game.map)
		return ([self.set_rabbit(who,x,y,game.rabbits[x][y]) for y in range(dim) for x in range(dim)]
			+ [self.set_map(who,x,y,game.map[x][y]) for y in range(dim) for x in range(dim)]
			+ [move_command.set_score(game), move_command.set_round(game.round[0])])


class finish_game_command(user_command):
	
	class finnish_msg(user_command):
		def __init__(self, winner):
			self.action = 'finish_game'
			self.user = ''
			self.winner = winner

		def process(self, game):
			pass
		
	""" zakoncz gre """
	def __init__(self):
		self.action = 'finish_game'
		self.user = ''
		self.winner = ''
	
	def validate(self, game, msg):
		return (msg['user']=='--hidden--')
	
	def process(self, game, msg):
		win_score = -1
		game.finished = True
		for p in game.players.iterkeys():
			sco = game.get_player_score(p)
			if sco>win_score:
				win_score = sco
				self.winner = game.players[p]
		return [move_command.set_round(-1), finish_game_command.finnish_msg(self.winner)]
		
class cancel_game_command(user_command):
	def __init__(self):
		None
		
	def validate(self, game, msg):
		return True
		
	def process(self, game, msg):
		color = -1
		print 'cancel game: ', msg, game.players
		for p in game.players.iterkeys():
			if game.players[p]==msg['user']:
				color = p
		print 'cancel game: ', color
		game.canceled[color] = True
		game.change_round()
		return [move_command.set_round(game.round[0])]

commands_map = {
	'move' : move_command,
	#'exit' : exit_command,
	'say' : say_command,
	'send_map' :  send_map_command,
	'cancel_game' : cancel_game_command,
	'finish_game' : finish_game_command
}

def process_message(game, msg):
	print "Process : ", msg['action']
	
	if (game.finished):
		return False
	
	proc = commands_map[msg['action']]()
	
	valid_round = (game.players[game.round[0]]==msg['user'])
	valid_round = True
	
	print "3"
	if valid_round and proc.validate(game, msg):
		msgs = proc.process(game, msg)
		cnt = len(msgs)
		for i in range(cnt):
			msgs[i].process(game)
			game.queue.add_message(msgs[i].__dict__, i==cnt-1)
		if (game.is_game_finished()):
			print "fisnih agame msg"
			fmsg = {'action':'finish_game', 'user':'--hidden--'}
			return process_message(game, fmsg)
		return True
	return False

