# IC 6200 1er Semestre 2016
# Nombre: <Su Nombre>
# Correo: <Su Correo>

from util import INFINITY

### 1. Escogencia multiple

# 1.1. Dos jugadores computarizados estan jugando un juego. E Jugador MM utiliza minimax
#      para buscar a una profundidad de 6 para decidir sobre una movida. El jugador AB utiliza alpha-beta
#      para buscar a una profundidad de 6.
#      El juego se lleva a cabo sin un limite de tiempo. Cual jugador jugara mejor?
#
#      1. MM jugara mejor que AB.
#      2. AB jugara mejor que  MM.
#      3. Ambos jugaran al mismo nivel de destreza.
ANSWER1 = 3

# 1.2. Dos jugadores computarizados juegan un juego con un limite de tiempo. El jugador MM
# hace busqueda minimax con profundidad iterativa, y el jugador AB hace busqueda alpha-beta
# con profundidad iterativa. Cada uno retorna un resultado despues de haber utilizado
# 1/3 de su tiempo restante. Cual jugador jugara mejor?
#
#      1. MM jugara mejor que AB.
#      2. AB jugara mejor que  MM.
#      3. Ambos jugaran al mismo nivel de destreza.
ANSWER2 = 2
### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## Esta seccion contiene lineas ocasionales que puede descomentar para jugar
## el juego interactivamente. Asegurese de re-comentar cuando ha terminado con
## ellos.  Por favor no entregue su tarea con partes de codigo que solicitan
## jugar interactivamente!
## 
## Descomente la siguiente linea para jugar el juego como las blancas:
#run_game(human_player, basic_player)

## Descomente la siguiente linea para jugar como las negras:
#run_game(basic_player, human_player)

## O bien vea a la computadora jugar con si misma:
#run_game(basic_player, basic_player)

## Cambie la siguiente funcion de evaluacion tal que trata de ganar lo mas rapido posible,
## o perder lentamente, cuando decide que un jugador esta destina a ganar.
## No tiene que cambiar como evalua posiciones que no son ganadoras.
def focused_evaluate(board):
    """
    Dado un tablero, returna un valor numerico indicando que tan bueno
    es el tablero para el jugador de turno.
    Un valor de retorno >= 1000 significa que el jugador actual ha ganado;
    Un valor de retorno <= -1000 significa que el jugador actual perdio
    """
    chain_cellsCurrent = board.chain_cells(board.get_current_player_id())
    chain_cellsOther = board.chain_cells(board.get_other_player_id())
    resultCurrent=0
    resultOther=0

    if (board.is_win()==board.get_current_player_id()):
        print "gano current"
        return 10000
    if board.is_win()==board.get_other_player_id():
        print "gano other"
        return -10000

    for i in chain_cellsCurrent:
        if len(i)>1:
            if i[0][0]==i[1][0]:
                if not is_blocked(i[0][0]-1,i[0][1],board):
                    if len(i)==2:
                        resultCurrent+=200
                    elif len(i)==3:
                        resultCurrent+=450
                print "i", i
                print "len(i)", len(i)
                print "i[len(i)-1][0]+1 ", i[len(i)-1][0]+1
                print "i[len(i)-1][1] ",i[len(i)-1][1]
                if not is_blocked(i[len(i)-1][1],i[len(i)-1][0]+1,board):
                    if len(i)==2:
                        resultCurrent+=200
                    elif len(i)==3:
                        resultCurrent+=450
            elif i[0][1]== i[1][1]:
                if not is_blocked(i[0][0],i[0][1]-1,board):

                    if len(i)==2:
                        resultCurrent+=200
                    elif len(i)==3:
                        resultCurrent+=450
            else:
                if (i[0][0]+1==i[1][0] and i[0][1]+1==i[1][1] ):
                    if not i[0][0]-1 <0 and not i[len(i)-1][0]+1>6 and not i[0][1]+1>5 and not i[len(i)-1][1]-1<0:
                         if not is_blocked(i[0][0]-1,i[0][1]+1,board):
                             if is_blocked(i[0][0]-1,i[0][1]+2,board):
                                 if len(i)==2:
                                    resultCurrent+=200
                                 elif len(i)==3:
                                    resultCurrent+=450
                         if not is_blocked(i[len(i)-1][0]+1,i[len(i)-1][1]-1,board):
                             if is_blocked(i[len(i)-1][0]+1,i[len(i)-1][1]-2,board):
                                 if len(i)==2:
                                    resultCurrent+=200
                                 elif len(i)==3:
                                    resultCurrent+=450
                else:
                    if not i[0][0]-1 <0 and not i[len(i)-1][0]-1<0 and not i[0][1]+1>5 and not i[len(i)-1][1]+1>6:

                        if not is_blocked(i[0][0]-1,i[0][1]-1,board):
                            if is_blocked(i[0][0]-1,i[0][1]-2,board):
                                if len(i)==2:
                                    resultCurrent+=200
                                elif len(i)==3:
                                    resultCurrent+=450

                        if not is_blocked(i[len(i)-1][1]+1,i[len(i)-1][0]+1,board):
                             if is_blocked(i[len(i)-1][0]-1,i[len(i)-1][1]+2,board):
                                 if len(i)==2:
                                    resultCurrent+=200
                                 elif len(i)==3:
                                    resultCurrent+=450
    for i in chain_cellsOther:

        if len(i)>1:
            if i[0][0]==i[1][0]:
                if not is_blocked(i[0][0]-1,i[0][1],board):
                    if len(i)==2:
                        resultOther+=200
                    elif len(i)==3:
                        resultOther+=450
                if not is_blocked(i[len(i)-1][1],i[len(i)-1][0] +1,board):
                    if len(i)==2:
                        resultOther+=200
                    elif len(i)==3:
                        resultOther+=450
            elif i[0][1]== i[1][1]:
                if not is_blocked(i[0][0],i[0][1]-1,board):

                    if len(i)==2:
                        resultOther+=200
                    elif len(i)==3:
                        resultOther+=450
            else:
                if (i[0][0]+1==i[1][0] and i[0][1]-1==i[1][1] ):
                    print "entrew!"
                    if not i[0][0]-1 <0 and not i[len(i)-1][0]+1>6 and not i[0][1]+1>5 and not i[len(i)-1][1]-1<0:
                         print  1
                         if not is_blocked(i[0][0]-1,i[0][1]+1,board):
                             print  2
                             print  "i[0][0]-1 ", i[0][0]-1
                             print "i[0][1]+2 ", i[0][1]+2
                             if is_blocked(i[0][0]-1,i[0][1]+2,board):
                                 print 3
                                 if len(i)==2:
                                    resultOther+=200
                                 elif len(i)==3:
                                    resultOther+=450
                         if not is_blocked(i[len(i)-1][1]-1,i[len(i)-1][0]+1,board):
                             if is_blocked(i[len(i)-1][0]+1,i[len(i)-1][1]-2,board):
                                 if len(i)==2:
                                    resultOther+=200
                                 elif len(i)==3:
                                    resultOther+=450
                else:
                    if not i[0][0]-1 <0 and not i[len(i)-1][0]-1<0 and not i[0][1]+1>5 and not i[len(i)-1][1]+1>6:

                        if not is_blocked(i[0][0]-1,i[0][1]-1,board):
                            if is_blocked(i[0][0]-1,i[0][1]-2,board):
                                if len(i)==2:
                                    resultOther+=200
                                elif len(i)==3:
                                    resultOther+=450

                        if not is_blocked(i[len(i)-1][0]+1,i[len(i)-1][1]+1,board):
                             if is_blocked(i[len(i)-1][0]-1,i[len(i)-1][1]+2,board):
                                 if len(i)==2:
                                    resultOther+=200
                                 elif len(i)==3:
                                    resultOther+=450

    if resultOther>resultCurrent:
        print "other", resultOther
        return -resultOther
    elif resultCurrent > resultOther:
        print "current",  resultCurrent
        return resultCurrent
    else:
        return 0




def is_blocked(x,y,board):
    print "x", x
    print "y", y
    if x<0 or x >6 or y<0 or y>5:
        return True
    elif board.get_cell(x,y)==0:
        return False
    return True


## Crea una funcion "jugador" que utiliza la funcion focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## Puede probar su nueva funcion de evaluacion descomentando la siguiente linea:
#run_game(basic_player, quick_to_win_player)

## Escriba un procedimiento de busqueda alpha-beta-search que actua como el procedimiento minimax-search
## pero que utiliza poda alpha-beta para evitar buscar por malas ideas
## que no pueden mejorar el resultado. El tester revisara la poda
## contando la cantidad de evaluaciones estaticas que hace
##
## Puede utilizar el minimax() que se encuentra basicplayer.py como ejemplo.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTA: usted debe utilizar get_next_moves_fn cuando genera
                      # configuraciones de proximos tableros, y utilizar is_terminal_fn para
                      # revisar si el juego termino.
                      # Las funciones que por defecto se asignan aqui funcionarar 
                      # para connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    raise NotImplementedError

## Ahora deberia ser capaz de buscar al doble de profundidad en la misma cantidad de tiempo.
## (Claro que este jugador alpha-beta-player no funcionara hasta que haya definido
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## Este jugador utiliza profundidad iterativa, asi que le puede ganar mientras hace uso 
## eficiente del tiempo:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finalmente, aqui debe crear una funcion de evaluacion mejor que focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the


## same depth.

def better_evaluate(board):
    raise NotImplementedError

# Comente esta linea una vez que ha implementado completamente better_evaluate
better_evaluate = memoize(basic_evaluate)

# Descomente esta linea para hacer que su better_evaluate corra mas rapido.
# better_evaluate = memoize(better_evaluate)

# Para el debugging: Cambie este if-guard a True, para hacer unit-test
# de su funcion better_evaluate.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate de jugador 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate de jugador 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## Un jugador que utiliza alpha-beta y better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Descomente para ver su jugador jugar un juego:
#run_game(your_player, your_player)

## Descomente esto (o corralo en una ventana) para ver como le va 
## en el torneo que sera evaluado.
#run_game(your_player, basic_player)

## Estas funciones son utilizadas por el tester, por favor no las modifique!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## Esta funcion corre su implementacion de alpha-beta utilizando un arbol de busqueda 
## en vez de un juego en vivo de connect four.   Esto sera mas facil de debuggear.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Quiere utilizar su codigo en un torneo con otros estudiantes? Vea 
## la descripcion en el enunciado de la tarea. El torneo es opcional
## y no tiene efecto en su nota
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""




def testGame():                       #0 1 2 3 4 5 6
   b = ConnectFourBoard(board_array=( (0,0,0,0,0,0,0), #0
                                      (0,0,0,0,0,0,0), #1
                                      (0,0,0,0,2,1,0), #2
                                      (0,0,0,2,1,1,0), #3
                                      (0,0,2,2,1,2,0), #4
                                      (0,0,2,1,1,1,2), #5
                                         ))
   print b.chain_cells(b.get_current_player_id())
   print b.chain_cells(b.get_other_player_id())
   focused_evaluate(b)


testGame()
