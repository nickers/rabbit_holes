# -*- coding: utf-8 -*-

from ajax_queue import *
from commands import *

class FT:
	EMPTY = 0
	HOLE  = 1
	BLOCK = 2
	BLACK = 10
	WHITE = 11

class game_state:
	
	__states = {}
	
	__dim = 6
	
	def __init__(self):
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
		
	
	def change_round(self):
		self.round = [self.round[(i+1)%len(self.round)] for i in range(len(self.round))]
	
	@staticmethod
	def get(game_id):		
		if not game_state.__states.has_key(game_id):
			game_state.__states[game_id] = game_state()
		return game_state.__states[game_id]
		
	@staticmethod
	def exists(game_id):
		return game_state.__states.has_key(game_id)
