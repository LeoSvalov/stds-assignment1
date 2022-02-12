from typing import List, Tuple


class Bucket:
    def __init__(self, epsilon: float):
        self.elements: List[Tuple] = []
        self.coverage: int = 0
        self.epsilon: float = epsilon

    def insert(self, v: float) -> None:
        index = next((i for i, element in enumerate(self.elements) if v < element[0]), len(self.elements))
        new_delta = 0
        if index != len(self.elements) and index != 0:
            new_delta = self.elements[index][1] + self.elements[index][2] - 1
        self.elements.insert(index, (v, 1, new_delta))
        self.coverage += 1
        if self.coverage % int(1 / (self.epsilon * 2)) == 0: self.merge()

    def merge(self) -> None:
        i = len(self.elements) - 1
        while i > 1:
            aggregated_g = self.elements[i][1]
            j = i - 1
            while j > 0 and aggregated_g + self.elements[j][1] + self.elements[i][2] < 2 * self.epsilon * self.coverage:
                aggregated_g += self.elements[j][1]
                j -= 1
            j += 1
            if j < i:
                self.elements = self.elements[:j] + [
                    (self.elements[i][0], aggregated_g, self.elements[i][2])] + self.elements[i + 1:]
            i = j - 1

    def query(self, q: float) -> float:
        q_r = int(q * self.coverage)
        r = 0
        for i, element in enumerate(self.elements):
            if i == 0: continue
            r += self.elements[i - 1][1]
            if r + self.elements[i][1] + self.elements[i][2] > int(self.epsilon * self.coverage) + q_r:
                return self.elements[i - 1][0]
        return self.elements[-1][0]



class SW:
    def __init__(self, N: int, epsilon: float):
        self.N: int = N
        self.epsilon: float = epsilon
        self.compressed_buckets: List[Bucket] = []
        self.active_bucket: Bucket = None

    def get_total_coverage(self):
        return sum([b.coverage for b in self.compressed_buckets])

    def insert(self, v: float) -> None:
        if self.active_bucket:
            self.active_bucket.insert(v)
            if self.active_bucket.coverage >= int(self.epsilon*self.N / 2):
                self.compress(self.active_bucket)
                self.active_bucket = None
        else: # no active bucket
            if self.get_total_coverage() < self.N: # check if we can add more buckets
                bucket = Bucket(epsilon=self.epsilon/4)
                bucket.insert(v)
                self.active_bucket = bucket
            else:
                self.compressed_buckets = self.compressed_buckets[:-1] # remove the oldest bucket
                self.insert(v)

    def compress(self, bucket: Bucket) -> Bucket:
        """
        transfer from (value, g, delta) notation to (value, r-, r+) (from original paper of this algo)
        """
        compressed_elements = []
        # add first element
        first_element = bucket.elements[0]
        first_element[2] += first_element[1]
        compressed_elements.append(first_element)
        r_minus = first_element[1]
        for i in range(1, min(int(2/self.epsilon)+1, len(bucket.elements)-1)):
            r_minus += bucket.elements[i][1]
            r_plus = r_minus + bucket.elements[i][2]
            # equation from the original paper
            if i*int(self.epsilon * self.N) - self.epsilon * self.N / 2 <= r_minus <= r_plus <= i*int(self.epsilon * self.N) + self.epsilon * self.N / 2:
                element = (bucket.elements[i][0],r_minus,r_plus)
                compressed_elements.append(element)

        # add last element
        last_element = bucket.elements[-1]
        r = sum([el[1] for el in bucket.elements])
        compressed_elements.append((last_element[0], r,r + last_element[2]))

        bucket.elements = compressed_elements
        bucket.coverage = len(compressed_elements)
        self.compressed_buckets.insert(0, bucket)

    def merge(self, q:float):
        pass
    def lift(self, merged_seq):
        pass
    def query(self, q: float):
        pass