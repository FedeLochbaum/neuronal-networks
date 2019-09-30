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
    left  = [ self.game[row-i][column-i] if(len(self.game) > row-i and len(self.game[row-i]) > column-i) else None for i in range(7)]
    right = [ self.game[row+i][column+i] if(len(self.game) <= row+i and len(self.game[row+i]) <= column+i) else None for i in range(7)]
    return self.check_four_contiguous(list(filter(lambda x: x != None, left + right)), player)

  def won_from_right_to_left(self, row, column, player):
    left  = [ self.game[row-i][column+i] if(len(self.game) > row-i and len(self.game[row-i]) <= column+i) else None for i in range(7)]
    right = [ self.game[row+i][column-i] if(len(self.game) <= row+i and len(self.game[row+i]) > column-i) else None for i in range(7)]
    return self.check_four_contiguous(list(filter(lambda x: x != None, left + right)), player)

  def check_four_contiguous(self, array, player):
    return functools.reduce(
      lambda acum, elem: acum + 1 if elem == player else 0,
      array, 0) >= 4
  
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

  