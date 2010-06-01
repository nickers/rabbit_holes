
from charades.game_state import game_state, FT
from commands import send_map_command, process_message

def ensure_game_exists(white_player, game_id=None):
	if not game_state.exists(game_id):
		game_id = game_state.create(game_id)
		print "Return game id ", game_id
		game = game_state.get(game_id)
		game.players[FT.WHITE] = white_player
		process_message(game, send_map_command('--system--').__dict__)
	return game_id
	

