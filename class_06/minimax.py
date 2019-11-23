from four_in_a_line import Game

from copy import deepcopy

MAX = 1
MIN = -1

def evaluate(game):
  return 1

def minimax(game, player):
  if game.game_over:
    score = evaluate(game)
    return (None, score)
  best = (None, player)
  valid_moves = game.valid_moves()
  print('valid moves for player', player, 'are: ', valid_moves)
  for move in valid_moves:
    next_node = deepcopy(game)
    next_node.put_in_column(move, player)
    next_score = minimax(next_node, -player)
    if player == MAX:
      if next_score[1] > best[1]:
        best = (move, next_score)
    elif next_score[1] < best[1]:
      best = (move, next_score)
  return best

game = Game(3, 4)
print(minimax(game, MAX))
