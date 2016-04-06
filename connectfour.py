import unicodedata
import sys

# Python 2.3 compatibiliy with sets
if not 'set' in globals():
    from sets import Set as set

def reverse(lst):
    """
    Invierte el orden de una lista.
    Muy similar en funcionalidad a la funcion de biblioteca 'reversed()'
    en versiones mas nuevas de Python.  Sin embargo, esta funcion trabaja con
    Python 2.3, y retorna una lista en vez de un generador.
    """
    retVal = list(lst)
    retVal.reverse()
    return retVal
    
def transpose(matrix):
    """ Transpone una matriz (definida como una lista de listas, donde cada sub-lista en una fila de la matrix) """
    # This feels dirty somewhow; but it does do exactly what I want
    return zip(*matrix)

class InvalidMoveException(Exception):
    """ Exception raised if someone tries to make an invalid move """
    def __init__(self, column, board):
        """
        'board' is the board on which the movement took place;
        'column' is the column to which an addition was attempted
        """
        self._column = column
        self._board = board

    def __str__(self):
        return "InvalidMoveException: Can't add to column %s on board\n%s" % (str(self._column), str(self._board))

    def __unicode__(self):
        return "InvalidMoveException: Can't add to column %s on board\n%s" % (unicode(self._column), unicode(self._board))

    def __repr__(self):
        return self.__str__()


class NonexistentMoveException(Exception):
    """ Raised if you try to request information on a move that does not exist """
    pass

    
class ConnectFourBoard(object):
    """ Store a Connect-Four Board

    Tableros Connect-Four son inmutabes; por favor no 
    sus habilidades Python para hackear/mutatarlos.  (No le dara ninguna ventaja;
    solo lograra que el tester deje de funcionar.)

    Un tablero Connect-Four board es una matriz, con la siguiente estructura:

         0 1 2 3 4 5 6 7
       0 * * * * * * * *
       1 * * * * * * * *
       2 * * * * * * * *
       3 * * * * * * * *
       4 * * * * * * * *
       5 * * * * * * * *
       6 * * * * * * * *

    Las columnas se llenan desde el fondo (ie., fila 6).
    """

    # El ancho horizontal del tablero
    board_width = 7
    # El alto vertical del tablero
    board_height = 6

    # Mapa de los numeros de ID para desplegar los caracteres utilizados para imprimir el tablero
    board_symbol_mapping = { 0: u' ',
                             1: unicodedata.lookup("WHITE SMILING FACE"),
                             2: unicodedata.lookup("BLACK SMILING FACE") }

    board_symbol_mapping_ascii = { 0: ' ',
                                   1: 'X',
                                   2: 'O' }
    
    def __init__(self, board_array = None, board_already_won = None, modified_column = None, current_player = 1, previous_move = -1):
        """ Crea un nuevo ConnectFourBoard

        Si se especifica el board_array, debe ser una matriz de MxN iterables
        (idealmente tuplas o listas), que seran utilizadas para describir el estado inicial
        del tablero.  Cada celda debe ser o bien '0', indicando desocupada, o
        N para algun entero correspondiente al numero del jugador.

        board_already_won puede opcionealmente setearse a None, o a el #id
        del jugador que a ganado el tablero.
        Si se especifica modified_column, debe ser el indice de la ultima columna
        en la que se dejo caer una ficha.
        Tanto board_already_won como modified_column son utilizados como pistas para la funcion
        'is_win_for_player()'.  Esta bien no especificarlos, pero sin son proveidos
        deben estar correctos.
        """
        if sys.stdout.encoding and 'UTF' not in sys.stdout.encoding: # If we don't support Unicode
            self.board_symbol_mapping = self.board_symbol_mapping_ascii
        
        if board_array == None:
            self._board_array = ( ( 0, ) * self.board_width , ) * self.board_height
        else:
            # Asegurandonos que guardamos tuplas, para que sean inmutables
            self._board_array = tuple( map(tuple, board_array) )

        #if board_already_won:
        #    self._is_win = board_already_won
        #elif modified_column:
        #    self._is_win = self._is_win_from_cell(self.get_height_of_column(modified_column), modified_column)
        #else:
        self._is_win = self.is_win()
            
        self.current_player = current_player

    def get_current_player_id(self):
        """ Retorna el id del jugador que le toca mover ahora """
        return self.current_player

    def get_other_player_id(self):
        """ Retorna el id del contrincante del jugador que le toca mover ahora """
        if self.get_current_player_id() == 1:
            return 2
        else:
            return 1
        
    def get_board_array(self):
        """ Retorna el array del tablero que representa este tablero (como una tupla de tuplas) """
        return self._board_array

    def get_top_elt_in_column(self, column):
        """
        Obtiene el #id del jugador que puso el ultimo token en la columna especificada.
        Retorna 0 si la columna se encuentra vacia.
        """
        for row in self._board_array:
            if row[column] != 0:
                return row[column]

        return 0

    def get_height_of_column(self, column):
        """
        Retorna el indice de la primera celda en la columna especificada que se encuentra con ficha
        Retorna ConnectFourBoard.board_height si la columna se encuentra vacia.
        """
        for i in xrange(self.board_height):
            if self._board_array[i][column] != 0:
                return i-1

        return self.board_height

    def get_cell(self, row, col):
        """
        Obtiene el  #id del jugador dueno de la ficha en la celda especificada.
        Retorna 0 si esta vacia.
        """
        return self._board_array[row][col]
    
    def do_move(self, column):
        """
        Ejecuta la movida especificada como el jugador actual.
        Retuorna un nuevo tablero con el resultado.
        genera 'InvalidMoveException' si la movida no es valida.
        """
        player_id = self.get_current_player_id()

        if self.get_height_of_column(column) < 0:
            raise InvalidMoveException(column, self)

        new_board = list( transpose( self.get_board_array() ) )
        target_col = [ x for x in new_board[column] if x != 0 ]
        target_col = [0 for x in xrange(self.board_height - len(target_col) - 1) ] + [ player_id ] + target_col

        new_board[column] = target_col
        new_board = transpose(new_board)

        # Re-immutablize the board
        new_board = tuple( map(tuple, new_board) )

        return ConnectFourBoard(new_board, board_already_won=self.is_win(), modified_column=column, current_player = self.get_other_player_id())

    def _is_win_from_cell(self, row, col):
        """ Determina si hay un conjunto ganador de cuatro nodos conectados que contiene la celda especificada """
        return ( self._max_length_from_cell(row, col) >= 4 )
        
    def _max_length_from_cell(self, row, col):
        """ Retorna el largo de la cadena mas larga que contiene esta celda """
        return max( self._contig_vector_length(row, col, (1,1)) + self._contig_vector_length(row, col, (-1,-1)) + 1,
                    self._contig_vector_length(row, col, (1,0)) + self._contig_vector_length(row, col, (-1,0)) + 1,
                    self._contig_vector_length(row, col, (0,1)) + self._contig_vector_length(row, col, (0,-1)) + 1,
                    self._contig_vector_length(row, col, (-1,1)) + self._contig_vector_length(row, col, (1,-1)) + 1 )

    def _contig_vector_length(self, row, col, direction):
        """
        Empezando en la celda especificada y contando en la direccion = (row_step, col_step),
        cuenta cuantas celdas consecutivas pertenecen al mismo jugador.
        """
        count = 0
        playerid = self.get_cell(row, col)

        while 0 <= row < self.board_height and 0 <= col < self.board_width and playerid == self.get_cell(row, col):
            row += direction[0]
            col += direction[1]
            count += 1

        return count - 1

    def longest_chain(self, playerid):
        """
        Retorna el largo de la cadena mas larga de fichas controlada por este jugador,
        0 si el jugador no tiene fichas en el tablero
        """
        longest = 0
        for i in xrange(self.board_height):
            for j in xrange(self.board_width):
                if self.get_cell(i,j) == playerid:
                    longest = max( longest, self._max_length_from_cell(i,j) )

        return longest

    def _contig_vector_cells(self, row, col, direction):
        """
        Emezando en la celda especificada y caminando en la direccion (row_step, col_step), cuenta cuantas
        celdas consecutivas son controladas por el mismo jugador que la el dueno de la celda inicial
        """
        retVal = []
        playerid = self.get_cell(row, col)

        while 0 <= row < self.board_height and 0 <= col < self.board_width and playerid == self.get_cell(row, col):
            retVal.append((row, col))
            row += direction[0]
            col += direction[1]

        return retVal[1:]

    def _chain_sets_from_cell(self, row, col):
        """ Retorna la cademna de max-length que contiene esta celda """
        return [ tuple(x) for x in [
                reverse(self._contig_vector_cells(row, col, (1,1))) + [(row, col)] + self._contig_vector_cells(row, col, (-1,-1)),
                 reverse(self._contig_vector_cells(row, col, (1,0))) + [(row, col)] + self._contig_vector_cells(row, col, (-1,0)),
                reverse(self._contig_vector_cells(row, col, (0,1))) + [(row, col)] + self._contig_vector_cells(row, col, (0,-1)),
                reverse(self._contig_vector_cells(row, col, (-1,1))) + [(row, col)] + self._contig_vector_cells(row, col, (1,-1)) 
                 ] ]

    def chain_cells(self, playerid):
        """
        Retorna un conjuto de todas las celdas en el tablero que son parte de una cada que esta controlada
        por el jugador especificado.

        El valor retorndo sera un set de Python que contiene las tuplas de las coordenadas.
        Por ejemplo, un valor de retorno puede verse como:

        set([ ( (0,1),(0,2),(0,3) ), ( (0,1),(1,1) ) ])

        Esto indicaria tokens contiguos desde (0,1)-(0,3) y (0,1)-(1,1).

        Las coordenadas dentro de una tupla estan debilmente ordenadas: cualesquiera coordenadas que son  
        adyecentes en la tupla tambien son adyecentes en el tablero.

        Note que fichas que se encuentras solas son cosideradas como cadenas de largo 1.  Esto es
        a veces util, pero a veces no; sin embargo, es relativamente facil eliminar 
        estos elementos por medio de comprension de listas o por medio de la funcion 'filter' de Python
        de la siguiente manera (por ejemplo):

        >>> my_big_chains = filter(lambda x: len(x) > 1, myBoard.chain_cells(playernum))

        Tambien recuerde que puede convertir este conjunto en una lista de la siguiente manera:

        >>> my_list = list( myBoard.chain_cells(playernum) )

        El valor de retorno se provee como un conjuto por los conjuntos son unicos y no-ordendos,
        como lo es esta coleccion de cadenas.
        """
        retVal = set()
        for i in xrange(self.board_height):
            for j in xrange(self.board_width):
                if self.get_cell(i,j) == playerid:
                    retVal.update( self._chain_sets_from_cell(i,j) )
                    
        return retVal
                    
        
    def is_win(self):
        """
        Retorna el #id del jugador que a ganado el juego.
        Retorna 0 si el juego no se ha ganado todavia.
        """
        #if hasattr(self, "_is_win"):
        #    return self._is_win
        #else:
        for i in xrange(self.board_height):
            for j in xrange(self.board_width):
                cell_player = self.get_cell(i,j)
                if cell_player != 0:
                    win = self._is_win_from_cell(i,j)
                    if win:
                        self._is_win = win
                        return cell_player

        return 0

    def is_game_over(self):
        """ Retorna True si el juego se ha ganado, False de otra manera """
        return ( self.is_win() != 0 or self.is_tie() )

    def is_tie(self):
        """ Retorna true sii el juego ha llegado a un punto muerto (nadie gana) """
        return not 0 in self._board_array[0]

    def clone(self):
        """ Retorna un duplicado de este objeto tablero """
        return ConnectFourBoard(self._board_array, board_already_won=self._is_win, current_player = self.get_current_player_id())

    def num_tokens_on_board(self):
        """
        Retorna el total de fichas (de cualquier jugador)
        que se encuentran en el tablero
        """
        tokens = 0

        for row in self._board_array:
            for col in row:
                if col != 0:
                    tokens += 1

        return tokens

    def __unicode__(self):
        """ Retorna una representacion en string del tablero """
        retVal = [ u"  " + u' '.join([str(x) for x in range(self.board_width)]) ]
        retVal += [ unicode(i) + ' ' + u' '.join([self.board_symbol_mapping[x] for x in row]) for i, row in enumerate(self._board_array) ]
        return u'\n' + u'\n'.join(retVal) + u'\n'

    def __str__(self):
        """ Retorna una representacion en strin del tablero  """
        retVal = [ "  " + ' '.join([str(x) for x in range(self.board_width)]) ]
        retVal += [ str(i) + ' ' + ' '.join([self.board_symbol_mapping_ascii[x] for x in row]) for i, row in enumerate(self._board_array) ]
        return '\n' + '\n'.join(retVal) + '\n'
        
    def __repr__(self):
        """ La representacion del tablero en hilera para el shell de Python """
        return self.__str__()

    def __hash__(self):
        """ Determina la llave hash del tablero.  La llave debe ser identica en dos tableros identicos. """
        return self._board_array.__hash__()

    def __eq__(self, other):
        """ Determina si dos tableros son iguales. """
        return ( self.get_board_array() == other.get_board_array() )

    
class ConnectFourRunner(object):
    """ Corre un juego de Connect Four.

    Las reglas de Connect Four son las mismas que las del juego real de Connect Four:

    * El juego es para dos jugadores.  Los jugadores se turnan para agregar una ficha en el tablero.
    * Cuando una ficha se agrega, el jugador decide en que columna se debe ubicar.
      la ficha "cae" a la posicion desocupada en la columna con el indice max grande.
    * El juego termina cuando alguno de los dos jugadores tiene cuatro fichas consecutivas en fila
      (ya sea horizonal, vertical, o diagonal en angulo de 45-grados), o cuando el tablero
      queda completamente lleno.  Si el juego termina con un jugador con 4 fichas consecutivas en linea,
      ese jugador es el ganador.
      
    EL game runner se implementa mediante callbacks:  Los dos jugadores especifican callbacks que son llamadas
    cuando les toca el turno.  Al callback se le pasan dos argumentos, self y self.get_board().
    La funcion debe devolver un valor dentro del tiempo especificado en (segundos) self.get_time_limit();
    en caso contrario el jugador correspondiente pierde!

    La funcion de callback debe retornar un entero correspondiente a la columna en la que quieren
    poner su ficha.
    """

    def __init__(self, player1_callback, player2_callback, board = ConnectFourBoard(), time_limit = 10):
        """ Create a new ConnectFourRunner.

        player1_callback y player2_callback son funciones de callback para los dos jugadores.
        board se inicializa al tablero de inicio, por defecto un ConnectFourBoard() generico.
        el time_limit es el tiempo (en segundos) disponible por jugador, por defecto 10 segundos.
        """
        self._board = board
        self._time_limit = time_limit     # timeout in seconds
        self.player1_callback = player1_callback
        self.player2_callback = player2_callback

    def get_board(self):
        """ Retorna el tablero actual """
        return self._board

    def get_time_limit(self):
        """ Retorna el imite de tiempo (en segundos) para funciones callback para este jugador """
        return self._time_limit

    def run_game(self, verbose=True):
        """ Run the test defined by this test runner.  Print and return the id of the winning player. """
        player1 = (self.player1_callback, 1, self._board.board_symbol_mapping[1])
        player2 = (self.player2_callback, 2, self._board.board_symbol_mapping[2])
        
        win_for_player = []

        while not win_for_player and not self._board.is_tie():            
            for callback, id, symbol in ( player1, player2 ):
                if verbose:
                    if sys.stdout.encoding and 'UTF' in sys.stdout.encoding:
                        print unicode(self._board)
                    else:
                        print str(self._board)

                has_moved = False

                while not has_moved:
                    try:
                        new_column = callback(self._board.clone())
                        print "Player %s (%s) puts a token in column %s" % (id, symbol, new_column)
                        self._board = self._board.do_move(new_column)
                        has_moved = True
                    except InvalidMoveException, e:
                        if sys.stdout.encoding and 'UTF' in sys.stdout.encoding:
                            print unicode(e)
                        else:
                            print str(e)
                            print "Illegal move attempted.  Please try again."
                            continue

                if self._board.is_game_over():
                    win_for_player = self._board.is_win()
                    break


        win_for_player = self._board.is_win()
                
        if win_for_player != 0 and self._board.is_tie():
            print "It's a tie!  No winner is declared."
            return 0
        else:
            self._do_gameend(win_for_player)
            return win_for_player

    def _do_gameend(self, winner):
        """ Aguien gano!  Nos encargaremos de esto eventualmente. """
        print "Win for %s!" % self._board.board_symbol_mapping[winner]
        if sys.stdout.encoding and 'UTF' in sys.stdout.encoding:
            print unicode(self._board)
        else:
            print str(self._board)


def human_player(board):
    """
    Un callback que le pregunta al usuario que hacer
    """
    target = None

    while type(target) != int:
        target = raw_input("Pick a column #: --> ")
        try:
            target = int(target)
        except ValueError:
            print "Please specify an integer column number"

    return target

        
def run_game(player1, player2, board = ConnectFourBoard()):
    """ Corre el juego de Connect Four, con los dos jugadores especificados """
    game = ConnectFourRunner(player1, player2, board=board)
    return game.run_game()
    
