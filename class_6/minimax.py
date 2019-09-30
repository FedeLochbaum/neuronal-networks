def minimax(node, player):
  if game_over(node):
    score = evaluate(node)
    return (None, score)
  best = (None, -inf if player == MAX else inf)
  for move in valid_moves(node):
    next_node = play(node, move)
    next_score = minimax(next_node, -player)
    if player == MAX:
      if next_score [2] > best [2]:
        best = (move, next_score)
    elif next_score [2] < best [2]:
        best = (move, next_score)
  return best
