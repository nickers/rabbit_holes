# -*- coding: utf-8 -*-
from twisted.web import resource, server
from twisted.internet import reactor, defer
import cPickle
import fcntl


dumper = cPickle
""" jako dumpera uzyjemy cPickle, by bylo szybciej """


class game_file:
	"""
		Plik ze stanem gry.
	"""


	__files_dir = u"./games_data/"
	"""Katalog do przechowywania stanów gry"""

	def __init__(self, game_id):
		self.id = unicode(game_id)
		self.file = self.__gen_file_name(game_id)
		self.info = {}

	def __gen_file_name(self, id):
		"""stwórz nazwę pliku według schematu"""
		return u"%s%s"%(self.__files_dir, unicode(self.id))

	def __load_file(self):
		if self.file:
			f = open(self.file)
			fcntl.flock(f, fcntl.LOCK_SH)
			self.info = dumper.load(f)
			fcntl.flock(f, fcntl.LOCK_UN)
			f.close()
		return None

	



	def render(self, request):
		""" Handle GET request, but don't finish it """
		print self.rqs, request
		if self.rqs:
			self.rqs.write("x")
			self.rqs.finish()
			self.rqs = None
		self.rqs = request
		return server.NOT_DONE_YET