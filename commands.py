# -*- coding: utf-8 -*-
from charades.game_state import game_state, FT

class user_command:
	def __init__(self):
		self.action = ""
		self.user = ""

class move_command(user_command):
	def validate(self, game):
		""" sprawdz czy ruch jest prawidlowy """
		return True

class say_command(user_command):
	
	class say_to_all(user_command):
		def __init__(self, msg):
			self.action = 'say'
			self.user = msg['user']
			self.msg = msg['msg']
	
	def validate(self, game, msg):
		""" sprawdz czy ruch jest prawidlowy """
		print 'Say: ', msg['msg']
		return True
	
	def process(self, game, msg):
		return [say_command.say_to_all(msg)]

class move_command(user_command):
	
	class add_rabbit(user_command):
		def __init__(self, who, x, y, c):
			self.action = 'add_rabbit'
			self.user = who
			self.x = x
			self.y = y
			self.color = c
	
	class del_rabbit(user_command):
		def __init__(self, who, x, y):
			self.action = 'del_rabbit'
			self.user = who
			self.x = x
			self.y = y
	
	def process(self, game, msg):
		dx = (int)(math.fabs(msg['srcX']-msg['dstX']))
		dy = (int)(math.fabs(msg['srcY']-msg['dstY']))
		who = game.players[game.round[0]]
		
		if (dx>=2 or dy>=2):
			ret = [add_rabbit(who, msg['dstX'], msg['dstY'], game.round[0])]
		else:
			return [del_rabbit(who, msg['srcX'], msg['srcY']),
					add_rabbit(who, msg['dstX'], msg['dstY'], game.round[0])]
		
	def validate(self, game, msg):
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
				over = game.rabbits[int((msg['srxX']+msg['dstX'])/2)][int((msg['srxY']+msg['dstY'])/2)]
				if over!=round:
					valid = False
			
		except: # mus be invalid position 
			valid = False
		
		return valid
		

commands_map = {
	'move' : move_command,
	#'exit' : exit_command,
	'say' : say_command
}

def process_message(game, msg):
	print msg
	proc = commands_map[msg['action']]()
	
	valid_round = (game.players[game.round[0]]==msg['user'])
	valid_round = True
	
	if valid_round and proc.validate(game, msg):
		msgs = proc.process(game, msg)
		cnt = len(msgs)
		for i in range(cnt):
			game.queue.add_message(msgs[i].__dict__, i==cnt-1)
		return True
	return False

