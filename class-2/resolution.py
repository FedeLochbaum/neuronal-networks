from graph import EightProblemGraph, current_target_position, compute_next_state, is_valid_position
from functools import reduce
import random
import copy
import gs
import a_star

######## Win node
win_node = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 0]
]
########

def position_of_value(value):
  for x in range(len(win_node)):
    for y in range(len(win_node[x])):
      if(win_node[x][y] == value):
        return x, y
  return None

def next_movement(direction, x, y):
  result = {
  'UP': lambda x, y: (x - 1, y),
  'DOWN': lambda x, y: (x + 1, y),
  'LEFT': lambda x, y: (x, y - 1),
  'RIGHT': lambda x, y: (x, y + 1),
  }
  return result[direction](x, y)

def checker(initialNode, solution):
  if(solution == None):
    return 'Fail'
  win_node, path, v = solution
  return simulate(initialNode, path) == win_node

def simulate(initialNode, movements):
  node = copy.deepcopy(initialNode)
  for direction in movements:
    x, y = current_target_position(node)
    newX, newY = next_movement(direction, x, y)
    if(is_valid_position((newX, newY, direction))):
      node = compute_next_state(node, newX, newY)
  return node

def generate_initial_node():
  new_node = copy.deepcopy(win_node)
  possible_movements = ['UP', 'DOWN', 'LEFT', 'RIGHT']
  movements = [random.choice(possible_movements) for i in range(100000)]
  return simulate(new_node, movements)

def number_of_wrong_numbers(node):
  accum = 0
  for x in range(len(node)):
    for y in range(len(node[x])):
      if(node[x][y] != win_node[x][y]):
        accum+=1
  return accum

# |𝑎−𝑐|+|𝑏−𝑑|
def manhattan_distance_of(current_value, x, y):
  correct_x, correct_y = position_of_value(current_value)
  return abs(x - correct_x) + abs(y - correct_y)
  

def sum_of_manhattan_distance(node):
  accum = 0
  for x in range(len(node)):
    for y in range(len(node[x])):
      accum+= manhattan_distance_of(node[x][y], x, y)
  return accum

# Al parecer, tanto number_of_wrong_numbers como sum_of_manhattan_distance son admisibles,
# en general, se basan en la representacion del tablero para calcular un numero exacto sin sobre estimar la lejania del estado actual al estado ganador

# Podemos decir que sum_of_manhattan_distance es dominante con respecto a number_of_wrong_numbers.
# number_of_wrong_numbers asigna como mucho valor 1 a cualquier posicion nodo del tablero que este en una posicion incorrecta,
# en cambio, sum_of_manhattan_distance en el mejor de los casos, para cualquier nodo en posicion incorrecta va a retornar 1, 
# pero en el caso general, la distancia manhattan para cualquier nodo incorrecto, va a retornar >1.

# En general, la heuristica sum_of_manhattan_distance suele encontrar mejores soluciones que number_of_wrong_numbers,
# tanto en cantidad de nodos visitados como en la longitud del path resultante. Aun asi, esto no siempre sucede, existen grafos en los cuales number_of_wrong_numbers consigue encontrar una solucion mas optima.

# Con respecto a los recorridos, se puede observar que GS consigue en menor cantidad de iteraciones (nodos visitados) una solucion para dicho problema, usando un recorrido que tiende mas a DFS.
# Sin embargo, A* Logra conseguir mejores resultados con respecto a la calidad de la solucion (caminos mas cortos) de lo cual se puede asumir que el recorrido generado tiende mas a BFS.
# Como se vio en clase, las soluciones generadas por A* suelen ser de mucha mejor calidad, pero habiendo explorado una cantidad considerable de nodos,
# a diferencia de GS que consigue soluciones no tan buenas generando una cantidad inferior de nodos.

# Ejemplo:
# Estado inicial:
# [8, 2, 5]
# [3, 1, 0]
# [4, 6, 7]

# GS con number_of_wrong_numbers:
#
# Longitud de la solucion: 143
#
# Cantidad de nodos visitados: 1737

# GS con sum_of_manhattan_distance:
#
# Longitud de la solucion: 93
#
# Cantidad de nodos visitados: 1115

# A* con number_of_wrong_numbers:
#
# Longitud de la solucion: 23
#
# Cantidad de nodos visitados: 48417

# A* con sum_of_manhattan_distance:
#
# Longitud de la solucion: 25
#
# Cantidad de nodos visitados: 17607

initial = generate_initial_node()
print('random initial state: ', str(initial))
print('\n')

gs_with_h1 = gs.gs(EightProblemGraph(), initial, number_of_wrong_numbers)
gs_with_h2 = gs.gs(EightProblemGraph(), initial, sum_of_manhattan_distance)
a_star_with_h1 = a_star.a_star(EightProblemGraph(), initial, number_of_wrong_numbers)
a_star_with_h2 = a_star.a_star(EightProblemGraph(), initial, sum_of_manhattan_distance)

print("GS with number_of_wrong_numbers: %s" % (gs_with_h1, ))
if gs_with_h1 != None:
  print('Count of visited nodes: ', gs_with_h1[2])
  print('Checker: ', checker(initial, gs_with_h1))
print('\n')

print("GS with sum_of_manhattan_distance: %s" % (gs_with_h2, ))
if gs_with_h1 != None:
  print('Count of visited nodes: ', gs_with_h2[2])
  print('Checker: ', checker(initial, gs_with_h2))
print('\n')

print("A* with number_of_wrong_numbers: %s" % (a_star_with_h1, ))
if a_star_with_h1 != None:
  print('Count of visited nodes: ', a_star_with_h1[2])
  print('Checker: ', checker(initial, a_star_with_h1))
print('\n')

print("A* with sum_of_manhattan_distance: %s" % (a_star_with_h2, ))
if a_star_with_h2 != None:
  print('Count of visited nodes: ', a_star_with_h2[2])
  print('Checker: ', checker(initial, a_star_with_h2))
print('\n')



