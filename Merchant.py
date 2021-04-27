# Import
from math import inf
from typing import Callable, Dict, List, Tuple
from random import choices, gauss


# Normal distribution within bounds with automatic sigma
def normal(lowBound: float, highBound: float, mu: float, sigma: float) -> int:
    x = round(gauss(mu, (highBound - lowBound) / sigma))
    if lowBound <= x and x <= highBound:
        return x
    return normal(mu, sigma, lowBound, highBound)


class Inventory:
    def __init__(self, name: str) -> None:
        self.name = name
        self.content: Dict[str, int] = {}
    
    def add(self, *other: Dict[str, int]) -> None:
        for i in other:
            for j in i:
                self.content[j] = self.content.get(j, 0) + i[j]

    def can_sub(self, other: Dict[str, int]) -> bool:
        return all(self.content.get(i, inf) >= other[i] for i in other)

    def sub(self, *other: Dict[str, int]) -> None:
        pass


    def move(self, other: Inventory, item: Dict[str, int]) -> None:
        self.sub(item)
        other.add(item)

    def __str__(self) -> str: return "{}:\n".format(self.name) + "\n".join(["{} x{}".format(i, self.content[i]) for i in sorted(self.content.keys())])


class PoolGen:
    def __init__(self, results: Dict[str, Tuple[float, ...]], method: Callable[..., int]) -> None:
        self.results = results
        self.method = method
    
    def roll(self, times: int = 1) -> List[Dict[str, int]]:
        return [{i: self.method(*self.results[i])} for i in choices([j for j in self.results], k=times)]


def equiPool(items: list[str], distribution: Tuple[float, ...], method: Callable[..., int]) -> PoolGen:
    return PoolGen({i: distribution for i in items}, method)




A = Inventory("Bag")

Fruits = equiPool(["Apple", "Orange", "Banana", "Rawsberry", "Citrus"], (2, 5, 3, 3), normal)
A.add(*Fruits.roll(10000))

print(A)