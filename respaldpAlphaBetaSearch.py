def alpha_beta_auxiliar(board, depth,alpha,beta,eval_fn,
                             get_next_moves_fn=get_all_next_moves,
                             is_terminal_fn=is_terminal):
    """
    Funcion de ayuda a Minimax: Retorna el valor minimax de un tablero particular,
    dado una profundidad con la cual estimar
    """
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    print "board en alpha beta aux"
    print board
    print "alpha"
    print alpha
    for move, new_board in get_next_moves_fn(board):
        alpha = max(alpha, alpha_beta_auxiliar(new_board,depth-1,alpha,beta,eval_fn,get_next_moves_fn,is_terminal_fn))
        if beta<=alpha:
            break
    return alpha
     
            
    """
    best_val = None
    
    for move, new_board in get_next_moves_fn(board):
        val = -1 * minimax_find_board_value(new_board, depth-1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn)
        if best_val == None or val > best_val:
            best_val = val

    return best_val"""

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
    Alpha= board
    Beta= board
    print "get_next_moves_fn(board)"
    print get_next_moves_fn(board)
    
    if is_terminal_fn(depth, board):
        return eval_fn(board)
    
    for move, nueva_jugada in get_next_moves_fn(board):
        Alpha = -1 * alpha_beta_auxiliar(nueva_jugada, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        if Beta == None or Alpha > Beta[0]:
            Beta = (Alpha, move, nueva_jugada)
    """else:
        for move, new_board in get_next_moves_fn(board):
            beta = min(alpha, alpha_beta_auxiliar(new_board,deph-1,alpha,beta,eval_fn,get_next_moves_fn,is_terminal_fn))
            if beta<=alpha:
                break
        return beta
    """
    
    """if(is_terminal_fn(depth,board) and depth==0):
        return eval_fn(board)    
        
    #Beta= None
    
    for move, nueva_jugada in get_next_moves_fn(board):
        Alpha = -1 * alpha_beta_auxiliar(nueva_jugada, depth-1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn)
        if Beta == None or Alpha > Beta[0]:
            Beta = (Alpha, move, nueva_jugada)
    """
    #print "JUgador"
    #print board.get_current_player_id()
    #print "Alpha beta decided"
    #print Beta[1]    
    #return Beta[1]
