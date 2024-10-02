from .search_algorithm import SearchAlgorithm
from structures.node import Node, MOVEMENTS
from state import State

class DepthFirstSearch(SearchAlgorithm):

    def __init__(self, initial:Node) -> None:
        self.opened_nodes = list([initial])
        self.closed_nodes = list()

        self.inital = initial

    @staticmethod
    def find_path(node:Node[State]):
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
    def expand_node(node:Node[State]):
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


    def get_next_move(self):
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
                
        return None