# -*- coding: utf-8 -*-

from ajax_queue import *

class game_state:
	
	__states = {}
	
	def __init__(self):
		self.queue = ajax_queue()
	
	@staticmethod
	def get(game_id):			
		if not game_state.__states.has_key(game_id):
			game_state.__states[game_id] = game_state()
		return game_state.__states[game_id]