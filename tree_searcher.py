#
# Este buscador de arboles utiliza el framework de juegos que tiene tarea2
# para correo busquedas alpha-beta en arboles estataticos de
#
#
# (See TEST_1 for an example tree.)
#
# En el directorio donde se encuentra tarea2.py corra:
#
#    ~> python tree_search.py
#
# Pero como prerequisito, su tarea2 debe implementar alpha_beta_search
# y la signatura de su funciones debe conformarse al interface
# definido abajo:
#
# def alpha_beta_search(board, depth,
#                       eval_fn,
#		        get_next_moves_fn,
#		        is_terminal_fn):
#
# En el contexto de arboles de busqueda:
#
# board es el nodo actual del arbol.
#
# depth es la profundidad de la busqueda.  Si especifica una profundidad muy grande
#   entonces su busqueda terminara en las hojas del arbol.
# 
# def eval_fn(board):
#   una funcion que retorna un puntaje para un tablero desde 
#   la perspectiva del jugador actual.
#
# def get_next_moves(board):
#   una funcion que toma un nodo actual (tablero) y genera
#   todas las proximas (move, newboard) tuplas posibles.
#
# def is_terminal_fn(depth, board):
#   es una funcion que revisa si se debe evaluar estaticamente
#   un tablero/node (por ende terminando la rama de busqueda).
#
# Usted puede cambiar el interface actual de su alpha_beta_search interface 
# para que trabaje con este interface definiendo su propio is_terminal_fn
# utilizando argumentos opcionales, de la siguiente manera:
#
# def alpha_beta_search(board, depth,
#                       eval_fn,
#                       get_next_moves_fn=get_all_next_moves,
#                       is_terminal_fn=<your_terminal_function>):

class Node:

    """
    Representacion de un nodo de juego generico.
    Cada nodo contiene
    1. una etiqueta
    2. un valor estatico (nodos internos 
    generalmente tiene un valor estatico de None)
    3. node type  {MIN, MAX}
    4. list of child nodes.
    """
    def __init__(self, label, value, node_type, children=[]):
        self.label = label
        self.value = value
        self.node_type = node_type
        self.children = children

    def set_children(self, child_nodes):
        """Setea los hijos de este nodo de arbol"""
        if not self.children:
            self.children = []
        for child in child_nodes:
            self.children.append(child)

    def get_children(self):
        return self.children

    def __str__(self):
        """Print el valor de este nodo."""
        if self.value is None:
            return self.label
        else:
            return "%s[%s]" %(self.label, self.value)

    def add(self, child):
        """Agrega hijos a este nodo."""
        if not self.children:
            self.children = []	    
            self.children.append(child)

    def num_children(self):
        """Cuantos hijos tiene este nodo?"""
        if self.children:
            return len(self.children)
        else:
            return 0

def tree_as_string(node, depth=0):
    """
    Genera una hilera que representa el arbol
    indentado con espacios
    """
    static_value = tree_eval(node)
    buf = "%s%s:%s\n" %(" "*depth, node.label, static_value)
    for elt in node.children:
        buf += tree_as_string(elt, depth+1)
    return buf

def make_tree(tup):
    """
    Genera un Nodo de arbol de una arbol formateado en tupla
    """
    return make_tree_helper(tup, "MAX")

def make_tree_helper(tup, node_type):
    """Genera un arbol de un formato tupla"""
    n = Node(tup[0], tup[1], node_type)
    children = []
    if len(tup) > 2:
        if node_type == "MAX":
            node_type = "MIN"
        else:
            node_type = "MAX"

    for c in xrange(2,len(tup)):
        children.append(make_tree_helper(tup[c], node_type))
    n.set_children(children)
    return n

def is_at_depth(depth, node):
    """
    is_terminal_fn para arboles de profundidad fija
    True si se ha llegado a depth == 0.
    """
    return depth <= 0

def is_leaf(depth, node):
    """
    is_terminal_fn para arboles de profundidad variable.
    Revisa si un nodo es un nodo hoja.
    """
    return node.num_children() == 0


def tree_get_next_move(node):
    """
    get_next_move_fn para arboles
    Retorna la lista de de proximas movidas para navegar por el arbol
    """
    return [(n.label, n) for n in node.children]

def tree_eval(node):
    """
    Retorna el valor estatic de un nodo
    """
    if node.value is not None:
        if node.node_type == "MIN":
            return -node.value
        elif node.node_type == "MAX":
            return node.value
        else:
            raise Exception("Unrecognized node type: %s" %(node.node_type))
    else:
        return None

def TEST_1(expected):
    from lab3 import alpha_beta_search
    tup_tree = ("A", None,
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
    )
    tree = make_tree(tup_tree)
    print "%s:\n%s" %("TREE_1", tree_as_string(tree))
    v = alpha_beta_search(tree, 10,
      tree_eval,
      tree_get_next_move,
      is_leaf)
    print "BEST MOVE:"
    print v
    print "EXPECTED:"
    print expected

def TEST_2(expected):
    from lab3 import alpha_beta_search
    tup_tree = ("A", None,
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
    )
    tree = make_tree(tup_tree)
    print "%s:\n%s" %("TREE_2", tree_as_string(tree))
    v = alpha_beta_search(tree, 10,
      tree_eval,
      tree_get_next_move,
      is_leaf)
    print "BEST MOVE:"
    print v
    print "EXPECTED:"
    print expected

def TEST_3(expected):
    from lab3 import alpha_beta_search
    tup_tree = ("A", None,
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
    )
    tree = make_tree(tup_tree)
    print "%s:\n%s" %("TREE_3",
    tree_as_string(tree))
    v = alpha_beta_search(tree, 10,
      tree_eval,
      tree_get_next_move,
      is_leaf)
    print "BEST-MOVE:"
    print v
    print "EXPECTED:"
    print expected

if __name__ == "__main__":
    # Corre tests basicos utilizando arboles.
    TEST_1("I")
    TEST_2("B")
    TEST_3("B")
