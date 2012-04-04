# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.web import static, server
from game import Game, GameCommandsWait, GameCommandProcess, CreateGameProcess, EnterGameProcess, LoginProcess, ListGamesProcess
from twisted.python import log
import sys
log.startLogging(sys.stdout)

root = static.File("./")
root.indexNames = [ 'index.html' ]

root.putChild('game', Game())
root.putChild('commands', GameCommandsWait())
root.putChild('send_command', GameCommandProcess())

root.putChild('create_game', CreateGameProcess())
root.putChild('enter_game', EnterGameProcess())

root.putChild('login', LoginProcess())
root.putChild('list_games', ListGamesProcess())

reactor.listenTCP(1080, server.Site(root))
reactor.run()

