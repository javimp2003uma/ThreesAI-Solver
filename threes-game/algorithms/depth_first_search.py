from .search_algorithm import SearchAlgorithm
from structures.node import Node, MOVEMENTS
from state import State

class DepthFirstSearch(SearchAlgorithm):

    def __init__(self, initial:Node) -> None:
        self.result, self.path, self.moves_list = self.run_algorithm(initial_state.clone_state())
        self.it = 0

    @staticmethod
    def find_path(node:Node):
        """
        Find path function based on node's father pointer
        """
        path = list()
        naux = node
        while(naux != None):
            path.insert(0,naux.father())
            naux = naux.father()(0)
        
        return path

    @staticmethod
    def expand_node(node:Node):
        """
        TODO
        Expand children from a node
        """
        children = list()

        aux : State = None

        # Up Movement
        aux = node.value.clone_state()
        aux.move_up()
        children.append(Node(aux, node, MOVEMENTS.UP))

        # Down Movement
        aux = node.value.clone_state()
        aux.move_down()
        children.append(Node(aux, node, MOVEMENTS.DOWN))

        # Left Movement
        aux = node.value.clone_state()
        aux.move_left()
        children.append(Node(aux, node, MOVEMENTS.LEFT))

        # Right Movement
        aux = node.value.clone_state()
        aux.move_right()
        children.append(Node(aux, node, MOVEMENTS.RIGHT))

        return children


    def run_algorithm(self, initial:Node):
        self.opened_nodes = list([initial])
        self.closed_nodes = list()

        self.inital = initial
        node:Node[State]

        while len(self.opened_nodes) != 0:
            node:Node[State] = self.opened_nodes.pop()
            self.closed_nodes.append(node)

            if node.value.completedState():
                return self.find_path(node)

            children = self.expand_node(node)

            for n in children:
                n:Node[State]=n
                if n not in self.closed_nodes and n not in self.opened_nodes:
                    self.opened_nodes.append(n)
                else:
                    pass
                
        return None

    def get_next_move(self):
        