import random
import math

class ErlangDistribution:

    k = 0           # order
    lam = 0         # rate

    def __init__(self, k, lam):
        self.lam = lam
        self.k = k
        if k == 0:
            raise Exception("Order parameter can't be less than 1!")
        if lam <= 0:
            raise Exception("Streaming rate can't be less or equal 0!")

    # Uses random (normal distribution) values to generate Erlang
    # random value
    def GenerateNext(self):
        res = 0
        for n in range(self.k - 1):
            if res != 0:
                res = random.random() * res
            else:
                res = random.random()
        res = 0 - (math.log(res) / self.lam)
        return res

    def GenerateNextInternal(self):
        return random.gammavariate(self.k, self.lam)

    def ChangeLambda(self, lam):
        self.lam = lam
