# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.web import static, server, script
from hello import *
from game import *

root = static.File("./")
root.putChild('test', Example())

root.putChild('game', Game())
root.putChild('commands', GameCommandsWait())
root.putChild('send_command', GameCommandProcess())

root.putChild('create_game', CreateGameProcess())
root.putChild('enter_game', EnterGameProcess())

root.putChild('login', LoginProcess())
root.putChild('list_games', ListGamesProcess())

#root.processors = { '.py': script.ResourceScript }
root.putChild("doc", static.File("/usr/share/doc"))
reactor.listenTCP(1080, server.Site(root))
reactor.listenTCP(80, server.Site(root))
reactor.run()

