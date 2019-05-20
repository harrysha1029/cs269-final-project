from pyquil import Program
from pyquil.gates import X, I, Y, Z
from secret import SecretShare

class HillerySecretShare2(SecretShare):
    """The second secret sharing protocol from
    Hillery, 1999"""
    def __init__(self):
        self.n = self.k = 2

    def split(self, secret):
        pass

    def recombine(self, shares):
        pass
