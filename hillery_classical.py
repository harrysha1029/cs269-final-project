"""
File: hillery1.py
Author: Harry Sha, Katy Woo
Description: Implements the first quantum secret sharing scheme
from Hillery et al. 1999.
"""
from pyquil.quilatom import QubitPlaceholder, MemoryReference
from pyquil.quil import address_qubits, DefGate
from pyquil import Program, get_qc
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE
from secret import SecretShare, Party
from pyquil.api import WavefunctionSimulator
from helpers import ghz, measure_X, measure_Y, assign
import numpy as np
from consts import *

sim = WavefunctionSimulator()

class Hillery1Party(Party):
    """ An honest party in the first secret
    sharing protocol.
    """
    def __init__(self, name):
        super().__init__(name)
        self.qubit = QubitPlaceholder()
        self.measurements = []
        self.directions = []
        self.key = []

    def interact(self, secret_share):
        """Interacts with the HillerySecretShare1
        object. In particular, it randomly samples a
        direction in which to measure and announces it
        """
        self.direction = num2direction[np.random.choice(2)]
        # # TEST A, B measure 'y'
        # self.direction = 'x' if self.name == 'C' else 'y'

        # # TEST A, B measure 'x'
        # self.direction = 'x'
        if self.direction == 'x':
            secret_share.program += measure_X(self.qubit, self.ro)
        else:
            secret_share.program += measure_Y(self.qubit, self.ro)
        secret_share.measure_list.append((self.name, self.direction))

# TODO Eavesdropper

class HillerySecretShare1(SecretShare):
    """The first secret sharing protocol from
    Hillery, 1999"""
    def __init__(self, parties):
        super().__init__(parties)
        self.A, self.B, self.C = self.parties
        self.qubits = [p.qubit for p in parties]
        self.init_program()
        self.qc = get_qc("3q-qvm")

    def init_program(self):
        """Initializes the pyquil program with the ghz
        state. Also resets the measure_list.
        """
        self.measure_list = []
        pq = ghz(self.qubits)
        ro = pq.declare('ro', memory_size=3)
        assign(ro, self.parties, 'ro')
        self.program = pq

    def check_valid(self):
        """Returns true if the the most recent measure_list
        is a valid one (one in which the honest parties
        can deduce the secret)
        """
        return tuple(self.measure_list) in VALID_DIRECTIONS

    def run(self, verbose=0):
        """ Measures the qubits after each
        party has announced their measurement direction.
        """
        if self.check_valid():
            if verbose==1: print('success')
            pq = address_qubits(self.program)
            result = self.qc.run(pq).flatten()
            for i, p in enumerate(self.parties):
                p.measurements.append(result[i])
                p.directions.append(self.measure_list)
            self.A.key.append(result[0])
        else:
            if verbose==1: print('execution failed')
            for p in self.parties:
                p.directions.append('fail')
                p.measurements.append('fail')
            result = None
        self.init_program()
        return result

def recombine(B, C):
    key = []
    for bit_ind, d in enumerate(B.directions):
        if d != 'fail':
            indexer = tuple([x[1] for x in d] + [C.measurements[bit_ind]])
            if B_IS_SAME_AS_A[indexer]:
                key.append(B.measurements[bit_ind])
            else:
                key.append(int(not(B.measurements[bit_ind])))

    B.key = C.key = key

def make_key(A, B, C, key_len=10):
    """
    Repeatedly runs the protocol
    to generate a secret for A such that
    B and C must cooperate to determine
    the secret
    """
    ss = HillerySecretShare1([A, B, C])
    n_valid = 0
    while n_valid < key_len:
        A.interact(ss)
        B.interact(ss)
        C.interact(ss)
        res = ss.run()
        if res is not None:
            n_valid += 1

    recombine(B, C)


if __name__ == '__main__':
    A, B, C = [Hillery1Party(x) for x in 'ABC']
    make_key(A, B, C, 20)
    print(A.key)
    print(B.key)
    print(C.key)



