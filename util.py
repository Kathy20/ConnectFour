from threading import Thread
from time import time
from connectfour import ConnectFourBoard
import tree_searcher

## Define 'INFINITY' and 'NEG_INFINITY'
try:
    INFINITY = float("infinity")
    NEG_INFINITY = float("-infinity")
except ValueError:                 # Windows no permite 'float("infinity")'.
    INFINITY = float(1e3000)       # Sin embargo, '1e3000' hara overflow y retornar
    NEG_INFINITY = float(-1e3000)  # el magico valor de float Infinity de todos modos.

class ContinuousThread(Thread):
    """
    Un hilo que corre una funcion continuamente,
    incrementando 'depth' kwarg, hasta que 
    un timeout especificado se ha excedido
    """

    def __init__(self, timeout=5, target=None, group=None, name=None, args=(), kwargs={}):
        """
        Store the various values that we use from the constructor args,
        then let the superclass's constructor do its thing
        """
        self._timeout = timeout
        self._target = target
        self._args = args
        self._kwargs = kwargs
        Thread.__init__(self, args=args, kwargs=kwargs, group=group, target=target, name=name)

    def run(self):
        """ Run until the specified time limit has been exceeded """
        depth = 1

        timeout = self._timeout**(1/2.0)  # Los tiempos crecen exponencialmente y no queremos 
                                          # empezar una nueva busqueda para la cual no vamos a tener
                                          # suficiente tiempo para terminarla

        end_time = time() + timeout
        
        while time() < end_time:
            self._kwargs['depth'] = depth
            self._most_recent_val = self._target(*self._args, **self._kwargs)
            depth += 1

    def get_most_recent_val(self):
        """ Retorna el valor mas reciente retornado por la funcion del thread """
        try:
            return self._most_recent_val
        except AttributeError:
            print "Error: You ran the search function for so short a time that it couldn't even come up with any answer at all!  Returning a random column choice..."
            import random
            return random.randint(0, 6)
    
def run_search_function(board, search_fn, eval_fn, timeout = 5):
    """
    Corre la funcion especificada de busqueda "search_fn" a profundidades crecientes
    hasta que  "time" ha expirado; entonces retorna el valor de retorno mas reciente

    "search_fn" debe tener los siguientes argumentos:
    board -- el tablero ConnectFourBoard a buscar
    depth -- la profundidad a la cual estimar
    eval_fn -- la funcion de evaluacion utilizada para rankear los nodos

    "eval_fn" debe tener el siguiente argumento:
    board -- el objeto ConnectFourBoard que se debe rankear
    """

    eval_t = ContinuousThread(timeout=timeout, target=search_fn, kwargs={ 'board': board,
                                                                          'eval_fn': eval_fn })

    eval_t.setDaemon(True)
    eval_t.start()
    
    eval_t.join(timeout)

    # Note que el thread puede que no se ejecute comiendose ciclos del CPU todavia;
    # Python no permite que los threads se puedan matar de manera significativa...
    return int(eval_t.get_most_recent_val())


class memoize(object):
    """
    decorador de 'Memoize'.

    Captura los valores de retorno de una funcion,
    tal que no hace falta computar el mismo output dos veces.

    Utilice asi:
    @memoize
    def my_fn(stuff):
        # Do stuff
    """
    def __init__(self, fn):
        self.fn = fn
        self.memocache = {}

    def __call__(self, *args, **kwargs):
        memokey = ( args, tuple( sorted(kwargs.items()) ) )
        if memokey in self.memocache:
            return self.memocache[memokey]
        else:
            val = self.fn(*args, **kwargs)
            self.memocache[memokey] = val
            return val


class count_runs(object):
    """
    decorador que cuenta corridas 'Count Runs'

    Cuenta cuantas veces la funcion decorada ha sido invocada.

    Utilice de la siguiente manera:
    @count_runs
    def my_fn(stuff):
        # Do stuff


    my_fn()
    my_fn()
    print my_fn.get_count()  # Prints '2'
    """

    def __init__(self, fn):
        self.fn = fn
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        self.fn(*args, **kwargs)

    def get_count(self):
        return self.count


    
# Algunos tableros de ejemplo, utiles para hacer testing:
# Gane obvio
WINNING_BOARD = ConnectFourBoard(board_array =
                                 ( ( 0,0,0,0,0,0,0 ),
                                   ( 0,0,0,0,0,0,0 ),
                                   ( 0,0,0,0,0,0,0 ),
                                   ( 0,1,0,0,0,0,0 ),
                                   ( 0,1,0,0,0,2,0 ),
                                   ( 0,1,0,0,2,2,0 ),
                                   ),
                                 current_player = 1)

# 2 puede ganar, pero 1 puede ganar con mucho mas facilidad
BARELY_WINNING_BOARD = ConnectFourBoard(board_array =
                                        ( ( 0,0,0,0,0,0,0 ),
                                          ( 0,0,0,0,0,0,0 ),
                                          ( 0,0,0,0,0,0,0 ),
                                          ( 0,2,2,1,1,2,0 ),
                                          ( 0,2,1,2,1,2,0 ),
                                          ( 2,1,2,1,1,1,0 ),
                                          ),
                                        current_player = 2)

BASIC_STARTING_BOARD_1 = ConnectFourBoard(board_array =
                                          ( ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,1,0,2,0,0 ),
                                            ),
                                          current_player = 1)

BASIC_STARTING_BOARD_2 = ConnectFourBoard(board_array =
                                          ( ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,0,0,0,0,0 ),
                                            ( 0,0,2,0,0,0,0 ),
                                            ( 0,0,1,0,0,0,0 ),
                                            ),
                                          current_player = 1)

# Tablero generico
BASIC_BOARD = ConnectFourBoard()

TEST_TREE_1 = tree_searcher.make_tree(("A", None,
                                       ("B", None,
                                        ("C", None,
                                         ("D", 2),
                                         ("E", 2)),
                                        ("F", None,
                                         ("G", 0),
                                         ("H", 4))
                                        ),
                                       ("I", None,
                                        ("J", None,
                                         ("K", 6),
                                         ("L", 8)),
                                        ("M", None,
                                         ("N", 4),
                                         ("O", 6))
                                        )
                                       ))

TEST_TREE_2 = tree_searcher.make_tree(("A", None,
                                       ("B", None,
                                        ("C", None,
                                         ("D", 6),
                                         ("E", 4)),
                                        ("F", None,
                                         ("G", 8),
                                         ("H", 6))
                                        ),
                                       ("I", None,
                                        ("J", None,
                                         ("K", 4),
                                         ("L", 0)),
                                        ("M", None,
                                         ("N", 2),
                                         ("O", 2))
                                        )
                                       ))

TEST_TREE_3 = tree_searcher.make_tree(("A", None,
                                       ("B", None,
                                        ("E", None,
                                         ("K", 8),
                                         ("L", 2)),
                                        ("F", 6)
                                        ),
                                       ("C", None,
                                        ("G", None,
                                         ("M", None,
                                          ("S", 4),
                                          ("T", 5)),
                                         ("N", 3)),
                                        ("H", None,
                                         ("O", 9),
                                         ("P", None,
                                          ("U", 10),
                                          ("V", 8))
                                         ),
                                        ),
                                       ("D", None,
                                        ("I", 1),
                                        ("J", None,
                                         ("Q", None,
                                          ("W", 7),
                                          ("X", 12)),
                                         ("K", None,
                                          ("Y", 11),
                                          ("Z", 15)
                                          ),
                                         )
                                        )
                                       ))



