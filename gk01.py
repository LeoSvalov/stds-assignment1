from typing import List, Tuple

"""
The very first choice of algorithm was Lin-SW. 
I have tried and consume quite a while implementing it, but got stuck in essence of merge operation.
So that, I switched to GK01 algo that used in Lin-SW.
"""


class GK01:
    def __init__(self, epsilon: float):
        self.elements: List[Tuple] = []
        self.coverage: int = 0
        self.epsilon: float = epsilon

    def insert(self, v: float) -> None:
        index = next((i for i, element in enumerate(self.elements) if v < element[0]), len(self.elements))
        new_delta = 0
        if index != len(self.elements) and index != 0:
            new_delta = self.elements[index][1] + self.elements[index][2]-1
        self.elements.insert(index, (v, 1, new_delta))
        self.coverage+=1
        if self.coverage % int(1 / (self.epsilon * 2)) == 0: self.merge()

    def merge(self) -> None:
        i=len(self.elements)-1
        while i>1:
            aggregated_g = self.elements[i][1]
            j = i-1
            while j>0 and aggregated_g + self.elements[j][1] + self.elements[i][2] < 2*self.epsilon * self.coverage:
                aggregated_g += self.elements[j][1]
                j -= 1
            j+=1
            if j<i:
                self.elements = self.elements[:j]+[(self.elements[i][0],aggregated_g,self.elements[i][2])]+self.elements[i+1:]
            i = j-1

    def query(self, q: float) -> float:
        q_r = int(q * self.coverage)
        r = 0
        for i, element in enumerate(self.elements):
            if i == 0: continue
            r += self.elements[i - 1][1]
            if r+self.elements[i][1]+self.elements[i][2] > int(self.epsilon * self.coverage)+q_r:
                return self.elements[i-1][0]
        return self.elements[-1][0]