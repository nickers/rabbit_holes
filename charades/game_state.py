# -*- coding: utf-8 -*-

from ajax_queue import *
from commands import *
import random

class FT:
	EMPTY = 0
	HOLE  = 1
	BLOCK = 2
	BLACK = 10
	WHITE = 11

class game_state:
	
	__states = {}
	
	__dim = 6
	
	def __init__(self, id):
		self.id = id
		self.queue = ajax_queue()
		self.map = [[FT.EMPTY for y in range(game_state.__dim)] for x in range(game_state.__dim)]
		self.map[0][game_state.__dim-1] = FT.BLOCK
		self.rabbits = [[FT.EMPTY for y in range(game_state.__dim)] for x in range(game_state.__dim)]
		for i in range(3):
			self.rabbits[0][game_state.__dim-2-i] = FT.WHITE
			self.rabbits[1+i][game_state.__dim-1] = FT.BLACK
		for i in range(game_state.__dim):
			self.map[i][0] = FT.HOLE
			self.map[game_state.__dim-1][i] = FT.HOLE
			
		self.players = {FT.WHITE:None, FT.BLACK:None}
		self.round = [FT.WHITE, FT.BLACK]
		self.canceled = {FT.WHITE:False, FT.BLACK:False}
		self.finished = False
		
	
	def change_round(self):
		"""
			False - koniec, nikt nie ma ruchów
			True - ok, kolejny gracz wybrany
		"""
		first_color = self.round[0]
		self.round = [self.round[(i+1)%len(self.round)] for i in range(len(self.round))]
		while first_color!=self.round[0] and (self.is_player_blocked(self.round[0]) or self.canceled[self.round[0]]):
			self.round = [self.round[(i+1)%len(self.round)] for i in range(len(self.round))]
		
		return first_color!=self.round[0]
		
	def is_valid_move(self, srcX, srcY, dstX, dstY):
		import math
		
		round = self.round[0]
		valid = True
		
		valid = srcX>=0 and srcY>=0 and dstX>=0 and dstY>=0
		valid = valid and srcX<game_state.__dim and srcY<game_state.__dim
		valid = valid and dstX<game_state.__dim and dstY<game_state.__dim

		try:
			srcColor = self.rabbits[srcX][srcY]
			dstColor = self.rabbits[dstX][dstY]
			
			srcMap = self.map[srcX][srcY]
			dstMap = self.map[dstX][dstY]
			
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
			
##			print "valid: %s " % (valid,)
			# move has valid vector
			dx = (int)(math.fabs(srcX-dstX))
			dy = (int)(math.fabs(srcY-dstY))
			validMoves = [(0,0),(1,0),(0,1),(1,1),(2,0),(0,2),(2,2)]
			try:
				validMoves.index((dx,dy))
			except: # invalid move
				valid = False
				
##			print "move validation: %s " % (valid,)
			
			# if jump then must jump over own color
			if dx==2 or dy==2:
				over = self.rabbits[int((srcX+dstX)/2)][int((srcY+dstY)/2)]
				if over!=round:
					valid = False
			
		except: # mus be invalid position
			valid = False
		
#		for y in range(6):
#			for x in range(6):
#				print self.rabbits[x][y], " ",
#			print ""
		
		return valid
	
	def is_player_blocked(self, color):
		for y in range(game_state.__dim):
			for x in range(game_state.__dim):
				for d in [(0,0),(1,0),(0,1),(1,1),(2,0),(0,2),(2,2)]:
					for m in [(1,1), (1,-1), (-1,-1), (-1,1)]:
						if self.is_valid_move(x,y,x+d[0]*m[0],y+d[1]*m[1]):
							return False
		return True
	
	def get_player_score(self, color):
		score = 0
		for y in range(game_state.__dim):
			for x in range(game_state.__dim):
				if self.map[x][y] == FT.HOLE and self.rabbits[x][y]==color:
					score = score +1
		return score
	
	def is_game_finished(self):
		game_end = True		
		for p in self.players.iterkeys():
			if not self.is_player_blocked(p) and not self.canceled[p]:
				game_end = False
		return game_end
				
	
	@staticmethod
	def get(game_id):		
		if not game_state.__states.has_key(game_id):
			#game_state.create(game_id)
			return None
		return game_state.__states[game_id]
		
	@staticmethod
	def exists(game_id):
		return game_state.__states.has_key(game_id)

	@staticmethod
	def create(game_id=None):
#		print "Create game: ", game_id		
		if game_state.exists(game_id):
			return False
		
		if (game_id==None):
			letters = "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
			game_id = ""
			for i in range(1,44):
				game_id = game_id + random.choice(letters)
		
		game_state.__states[game_id] = game_state(game_id)
#		print "  --> ", game_id
		return game_id

	@staticmethod
	def destroy(game_id):
		if (game_state.exists(game_id)):
			game_state.__states.pop(game_id)

	@staticmethod
	def list():
		return game_state.__states.keys()

