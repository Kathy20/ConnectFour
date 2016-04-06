# IC 6200 1er Semestre 2016
# Nombre: Kathy Brenes Guerrero
# Correo: KathyBG.20@gmail.com

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
def is_horizontal(chain):
    if chain[0][0]==chain[1][0]:
        return True
    else:
        return False

def rev_horizontal(board,chain,playerID,enemy):
    #Si es horizontal reviso que no este bloqueado
    #ni a la derecha ni a la izquierda
    #print "Es horizontal"
    score=0
    #Revisar si al final de la horizontal esta bloqueada,
    #sino si alcanza para llegar a 4
    if not is_block(board,chain[0][0],chain[0][1]+1,enemy):
        #print "Entre a no esta bloqueada la primera de la ultima"
        if not is_block(board,chain[0][0],chain[0][1]+2,enemy):
            #Tengo dos casillas disponibles
            score= score + 300
        score= score + 300;
        #print "NO esta bloqueada"
        #print score
     

    ##### Revisa si el inicio de la hilera horizontal esta bloqueada
    if not is_block(board,chain[0][0],chain[len(chain)-1][1]-1,enemy):
        if not is_block(board,chain[0][0],chain[len(chain)-1][1]-2,enemy):
            #Se tienen dos posibles casillas antes de la hilera
            score= score + 300;
        #print"No esta bloqueada"
        score= score + 300;
    
    return score

def is_vertical(chain):
    ##Revisa si la cadena de fichas esta colocada verticalmente
    if chain[0][1]==chain[1][1]:
        return True
    else:
        return False
    
def rev_vertical(board,chain,playerID,enemy):
    #Si es vertical reviso que no este bloqueado
    #ni arriba ni abajo
    #print "Es vertical"
    score=0 
    ##### Revisar si el de mas arriba se encuentra bloqueado
    if not is_block(board,chain[len(chain)-1][0]-1,chain[len(chain)-1][1],enemy):
        if not is_block(board,chain[len(chain)-1][0]-2,chain[len(chain)-1][1],enemy):
            #Se tienen dos posibles casillas antes de la hilera
            score= score + 300;
        #print"No esta bloqueada"
        score= score + 300;
        
    return score

def rev_diagonal(board,chain,playerID):
    #Si es diagonal reviso que no este bloqueado
    #ni arriba adelante o arriba atras ni abajo atras ni abajo adelante
    #print "Es diagonal"
    score=0 
    ##### Revisar si el de mas abajo atras se encuentra bloqueado   
    if is_free(board,chain[0][0]+1,chain[0][1]-1):
        if is_free(board,chain[0][0]+2,chain[0][1]-2):
            #Se tienen dos posibles casillas antes de la hilera
            score= score + 150;
        #print"No esta bloqueada"
        score= score + 150;
    
        
    ##### Revisar si el de mas abajo adelante se encuentra bloqueado   
    if is_free(board,chain[0][0]+1,chain[0][1]+1):
        if is_free(board,chain[0][0]+2,chain[0][1]+2):
            #Se tienen dos posibles casillas antes de la hilera
            score= score + 150;
        #print"No esta bloqueada"
        score= score + 150;
       
    ##### Revisar si el de mas arriba atras se encuentra bloqueado   
    if is_free(board,chain[0][0]-1,chain[0][1]-1):
        if is_free(board,chain[0][0]-2,chain[0][1]-2):
            #Se tienen dos posibles casillas antes de la hilera
            score= score + 150;
        #print"No esta bloqueada"
        score= score + 150;
         
    ##### Revisar si el de mas arriba adelante se encuentra bloqueado   
    if is_free(board,chain[0][0]-1,chain[0][1]+1):
        if is_free(board,chain[0][0]-1,chain[0][1]+2):
            #Se tienen dos posibles casillas antes de la hilera
            score= score + 150;
        #print"No esta bloqueada"
        score= score + 150;
    
    #### Revisa si el de mas adelante
    return score

############################################
# Is_Block revisa si una celda esta utilizada
def is_block(board,fila,columna,enemyID):
    if columna<0 or columna >6 or fila<0 or fila>5:
        return True
    elif board.get_cell(fila,columna)==enemyID:
        return True
    return False

# Is_Free revisa si una celda esta utilizada
def is_free(board,fila,columna):
    if columna<0 or columna >6 or fila<0 or fila>5:
        return False
    elif board.get_cell(fila,columna)==0:
        return True
    return False

def focused_evaluate(board):
    """
    Dado un tablero, returna un valor numerico indicando que tan bueno
    es el tablero para el jugador de turno.
    Un valor de retorno >= 1000 significa que el jugador actual ha ganado;
    Un valor de retorno <= -1000 significa que el jugador actual perdio
    """
    playerID= board.get_current_player_id()
    enemy = board.get_other_player_id()
    score=0
    if board.is_game_over():
        # Si el juego ha sido ganado, se tiene que saber si es a
        # favor nuestro o del oponente
        if board.is_win()== playerID:
            score = 100000
        else:
            score = -100000
    else:        
        chains= board.chain_cells(playerID)
        for chain in chains:            
            if len(chain)>1:
                if is_horizontal(chain):
                    score= score+rev_horizontal(board,chain,playerID,enemy)                    
                elif is_vertical(chain):
                    #Revisa si esta bloqueado arriba o abajo
                    score= score+rev_vertical(board,chain,playerID,enemy) 
                else:
                    #Es diagonal
                    score= score + rev_diagonal(board,chain,playerID)

        chainsAgainst= board.chain_cells(enemy)
        for against in chainsAgainst:
            #print against
            if len(against)>1:
                if is_horizontal(against):
                    score= score-rev_horizontal(board,against,enemy,playerID)                    
                elif is_vertical(against):
                    #Revisa si esta bloqueado arriba o abajo
                    score= score-rev_vertical(board,against,enemy,playerID) 
                else:
                    #Es diagonal
                    score= score - rev_diagonal(board,against,enemy)        
    return score



## Crea una funcion "jugador" que utiliza la funcion focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## Puede probar su nueva funcion de evaluacion descomentando la siguiente linea:
run_game(basic_player, quick_to_win_player)

## Escriba un procedimiento de busqueda alpha-beta-search que actua como el procedimiento minimax-search
## pero que utiliza poda alpha-beta para evitar buscar por malas ideas
## que no pueden mejorar el resultado. El tester revisara la poda
## contando la cantidad de evaluaciones estaticas que hace
##
## Puede utilizar el minimax() que se encuentra basicplayer.py como ejemplo.
##########funcion minimax para el alpha beta
def minimax(board, depth, eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Funcion de ayuda a Minimax: Retorna el valor minimax de un tablero particular,
    dado una profundidad con la cual estimar
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)

    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * minimax_find_board_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
        if best_val == None or val > best_val:
            best_val = val

    return best_val

##############
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTA: usted debe utilizar get_next_moves_fn cuando genera
                      # configuraciones de proximos tableros, y utilizar is_terminal_fn para
                      # revisar si el juego termino.
                      # Las funciones que por defecto se asignan aqui funcionarar 
                      # para connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
    
    #Debe retornar el numero de columna
    #alpha limite inferior
    #beta limite superior
    if(is_terminal_fn(depth,board) and depth==0):
        return eval_fn(board)    
        
    Beta= None
    
    for move, nueva_jugada in get_next_moves_fn(board):
        Alpha = -1 * minimax(nueva_jugada, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        if Beta == None or Alpha > Beta[0]:
            Beta = (Alpha, move, nueva_jugada)
            
    print "Alpha beta decided"
    print Beta[1]    
    return Beta[1]
    
    

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



def testGame():                      # 0 1 2 3 4 5 6
   b = ConnectFourBoard(board_array=( (0,0,0,0,0,0,0), #0
                                      (0,0,0,0,0,0,0), #1
                                      (0,0,0,0,0,0,0), #2
                                      (0,0,0,0,0,0,0), #3
                                      (0,0,0,2,1,2,0), #4
                                      (0,0,2,1,1,1,2), #5
                                         ))
   print focused_evaluate(b)
   print "Ahora vamos con d"
   #                                   0 1 2 3 4 5 6
   d = ConnectFourBoard(board_array=( (0,0,0,0,0,0,0), #0
                                      (0,0,0,0,0,0,0), #1
                                      (0,0,0,0,0,0,0), #2
                                      (2,0,0,0,1,1,0), #3
                                      (2,2,0,1,1,2,0), #4
                                      (2,2,2,1,1,1,0), #5
                                         ))
   print focused_evaluate(d) 
## Quiere utilizar su codigo en un torneo con otros estudiantes? Vea 
## la descripcion en el enunciado de la tarea. El torneo es opcional
## y no tiene efecto en su nota
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "25"
WHAT_I_FOUND_INTERESTING = "Calcular las posibles jugadas en un momento dado."
WHAT_I_FOUND_BORING = "Correr las pruebas, porque generalmente toma mucho tiempo."
NAME = "Kathy Brenes Guerrero"
EMAIL = "Kathy.20@hotmail.es"

#testGame();
