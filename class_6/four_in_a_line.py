import functools

initial_value = 0
def next(player_tag):
  if('x' == player_tag):
    return 'y'
  return 'x'

def play():
  game = Game()
  print('\n')
  print('Welcome to 4 in a line! (?')
  turn = next('y')
  game.show()
  while(not game.game_over):
    print('Turn of ', turn, ' select some column')
    print('\n')
    column = int(input())
    game.put_in_column(column, turn)
    game.show()
    turn = next(turn)
  print('Player ', next(turn), 'won!')

class Game:
  def __init__(self, rows_number = 6, columns_number = 7):
    self.game_over = False
    self.columns_number = columns_number
    self.rows_number = rows_number
    self.game = [ [ initial_value for y in range(columns_number) ] for x in range(rows_number) ]

  def won_in_same_horizontal(self, row, player):
    return self.check_four_contiguous(self.game[row], player)

  def won_in_vertical(self, column, player):
    return self.check_four_contiguous([row[column] for row in self.game], player)

  def won_in_diagonal(self, row, column, player):
    return self.won_from_left_to_right(row, column, player) or self.won_from_right_to_left(row, column, player)

  def won_from_left_to_right(self, row, column, player):
    left  = self.nodes_from_top_right_to_down_left(row + 1, column - 1)
    right = self.nodes_from_down_left_to_top_right(row - 1, column + 1)
    l = list(filter(lambda x: x != None, left + [self.game[row][column]] + right))
    return self.check_four_contiguous(l, player)

  def won_from_right_to_left(self, row, column, player):
    left  = self.nodes_from_down_right_to_top_left(row - 1, column - 1)
    right = self.nodes_from_top_left_to_down_right(row + 1, column + 1)
    l = list(filter(lambda x: x != None, left + [self.game[row][column]] + right))
    return self.check_four_contiguous(l, player)

  def nodes_from_top_right_to_down_left(self, row, column):
    # row + 1, column - 1
    res = []
    while(self.is_valid_position(row, column)):
      res.append(self.game[row][column])
      row +=1
      column -=1
    return res

  def nodes_from_down_left_to_top_right(self, row, column):
    # row - 1, column + 1
    res = []
    while(self.is_valid_position(row, column)):
      res.append(self.game[row][column])
      row -=1
      column +=1
    return res

  def nodes_from_down_right_to_top_left(self, row, column):
    # row - 1, column - 1
    res = []
    while(self.is_valid_position(row, column)):
      res.append(self.game[row][column])
      row -=1
      column -=1
    return res

  def nodes_from_top_left_to_down_right(self, row, column):
    # row + 1, column + 1
    res = []
    while(self.is_valid_position(row, column)):
      res.append(self.game[row][column])
      row +=1
      column +=1
    return res

  def is_valid_position(self, row, column):
    return (row >= 0 and row <= self.rows_number - 1) and (column >= 0 and column <= self.columns_number - 1)

  def check_four_contiguous(self, array, player):
    maxs = [0]
    current_max = 0
    for elem in array:
      if(elem == player):
        current_max += 1
      else:
        maxs.append(current_max)
        current_max = 0
    return max(maxs) >= 4
  
  def check_game_state(self, row, column, player):
    self.game_over = (
      self.won_in_same_horizontal(row, player) or 
      self.won_in_vertical(column, player) or 
      self.won_in_diagonal(row, column, player))

  def show(self):
    print('\n')
    for row in self.game:
      [print('|', cell, '', end = '') for cell in row ]
      print('|', end = '')
      print('')
    print('-----------------------------')

  def put_in_column(self, column, player):
    for i in reversed(range(self.rows_number)):
      if (self.game[i][column] == initial_value):
        self.game[i][column] = player
        self.check_game_state(i, column, player)
        return

play()

  