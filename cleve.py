from pyquil import Program
from pyquil.gates import X, I, Y, Z
from secret import SecretShare

class CleveSecretShare(SecretShare):
    """The secret sharing protocol from
    Cleve, 1999"""
    def __init__(self, n, k):
        super(CleveSecretShare, self).__init__(n, k) #self.n, k

    def split(self, secret):
        pass

    def recombine(self, shares):
        pass
