from enum import Enum


class MOVEMENTS(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Node[T]:

    def __init__(self, value: T, father, movement:MOVEMENTS) -> None:
        self.value = value
        if father != None and movement != None:
            self.father = (father,movement)


    def value(self) -> T:
        return self.value
    
    def father(self) -> tuple[any, MOVEMENTS]:
        return self.father

    
