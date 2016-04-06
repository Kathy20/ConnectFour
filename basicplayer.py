from util import memoize, run_search_function

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # Si el juego ha sido ganado, sabemos que debe haber sido
        # ganado o terminado en la movida anterior.
        # La jugada anterior fue efectuada por nuestro oponente.
        # Por lo que no podemos haber ganado, asi que retornamos -1000.
        # (note que esto produce que un empate sea tratado como una perdida)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefiere poner sus piezas en el centro del tablero
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Retorna un generador de todas las movidas que el jugador actual puede hacer desde esta posicion"""
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Revision generica de si estado es terminal, retorna True cuando la se alcanza la maxima profundidad o
    el juego ha terminado
    """
    return depth <= 0 or board.is_game_over()
    
def minimax_find_board_value(board, depth, eval_fn,
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

def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    """
    Hace una busqueda minimax en el tablero a la profundidad especificada.

    board -- la instancia ConnectFourBoard a evaluar
    depth -- la profundidad del arbol de busqueda (medida como la distancia maxima de la raiz a una hoja)
    eval_fn -- (opcional) la funcion de evaluacion para utilizar en una hoja del arbol; revise "focused_evaluate" para ver un ejemplo
    
    Returna un entero, el numero de columna que la busqueda indica donde debe agregar su ficha
    """
    
    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * minimax_find_board_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)
            
    if verbose:
        print "MINIMAX: Decided on column %d with rating %d" % (best_val[1], best_val[0])

    return best_val[1]


basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
