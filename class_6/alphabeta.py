def alphabeta(node, depth, alpha, beta, player):
  if depth == 0 or game_over(node):
    return h(node)
  if player == MAX:
    value = -inf
    for move in valid_moves(node):
      child = play(node, move)
      value = max(value, alphabeta(child, depth - 1, alpha, beta, -player))
      alpha = max(alpha, value)
      if alpha >= beta:
        break # beta cut - off
    return value
  else:
    value = inf
    for move in valid_moves(node):
      child = play(node, move)
      value = min(value, alphabeta(child, depth - 1, alpha, beta, -player))
      beta = min(beta, value)
      if alpha >= beta:
        break # alpha cut - off
  return value
