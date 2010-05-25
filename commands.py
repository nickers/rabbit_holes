# -*- coding: utf-8 -*-

class user_command:
	def __init__(self):
		self.action = ""
		self.username = ""

class move_command(user_command):
	def validate(self, game):
		""" sprawdz czy ruch jest prawidlowy """
		return True

class say_command(user_command):
	def validate(self, game):
		""" sprawdz czy ruch jest prawidlowy """
		print self.message
		return True


commands_map = {
	'move' : move_command,
	'say' : say_command
}