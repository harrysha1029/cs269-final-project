"""
File: cleve.py
Author: Harry Sha, Katy Woo
Description: Implements a simulation of
Cleve's multiparty quantum secret sharing scheme.
"""
import numpy as np
from sympy import sieve
from sympy import Matrix
from secret import SecretShare
from cleve_setup import create_poly_state, num2bin
from secret import Party


class CleveParty(Party):
    """ An honest party in the first secret
    sharing protocol.
    """
    def __init__(self, name):
        super().__init__(name)


class CleveSecretShare(SecretShare):
    """The secret sharing protocol from
    Cleve, 1999"""
    def __init__(self, parties, k):
        super().__init__(parties, k)
        assert self.k <= self.n

    def get_q(self, s):
        """Computes the order of the base field,
        q, and sets the variables, self.q, self.b_len.
        b_len is the number of qubits used to simulate a single
        state, which is required as pyquil currently does not
        directly support this.
        """
        self.q = sieve.primerange(max(self.n, s), 2*max(self.n, s)).__next__()
        l = np.log2(self.q)
        self.b_len = int(l) +1
        return self.q

    def split(self, secret):
        """Splits a secret state into
        self.n shares.
        """
        states = [s[0] for s in secret]
        alphas = [s[1] for s in secret]
        self.get_q(max(states))
        self.sum_state, self.count_vec = create_poly_state(
            states, alphas, self.q, self.n, self.k)

    def recombine(self, parties):
        """
        Given a list of parties, reconstructs
        the secret
        """

        parties = [p.name for p in parties]
        # Only use k parties is more are given
        if len(parties) > self.k:
            parties = parties[:self.k]
        if len(parties) < self.k:
            raise Exception

        not_party = [i for i in range(1,self.n+1) if i not in parties]

        parties = sorted(parties)
        V = Matrix(np.vander(parties, increasing=True))
        V_inv = V.inv_mod(self.q)
        V_2 = Matrix(np.vander(not_party, increasing=True))
        state = {}

        # Apply Vandermonde matrices, and move registers around
        for k in self.count_vec:
            y = np.array([int(k[(i-1)*self.b_len:i*self.b_len], 2) for i in parties])
            state[k] = np.mod(np.array(V_inv * Matrix(y)).astype(np.int).flatten(), self.q)
            state[k] = np.roll(state[k], 1)
            temp = state[k][0]
            state[k] = np.mod(np.array(V_2 * Matrix(state[k][1:])).astype(np.int).flatten(), self.q)
            state[k] = np.mod([s + temp*n**(self.k-1) for s,n in zip(state[k], not_party)], self.q)
            state[k] = np.insert(state[k], 0, temp)

        # Update count_vec: switch keys out with the things mapped to by state.
        count_after_map = {}
        for k, v in self.count_vec.items():
            if k in state:
                new_k = ''
                for p in range(1, self.n+1):
                    if p in parties:
                        s = state[k][parties.index(p)]
                        new_k += num2bin(s, self.b_len)
                    else:
                        new_k += k[(p-1)*self.b_len:p*self.b_len]
            else:
                new_k = k
            count_after_map[new_k] = v

        return count_after_map


if __name__ == '__main__':
    parties = [CleveParty(x) for x in range(1, 6)]
    x = CleveSecretShare(parties, 3)
    x.split([(1, 4/5), (3, 3/5j)])
    print(x.recombine(parties[:3]))
