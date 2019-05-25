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

N = 3
sim = WavefunctionSimulator()
qc = get_qc("5q-qvm")

class Hillery1Party(Party):
    def __init__(self, name):
        Party.__init__(self, name)
        self.qubit = QubitPlaceholder()
        self.key = []

    def interact(self, secret_share):
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

class HillerySecretShare1(SecretShare):
    """The first secret sharing protocol from
    Hillery, 1999"""
    def __init__(self, parties):
        super().__init__(parties)
        self.qubits = [p.qubit for p in parties]
        self.measure_list = []
        self.init_program()

    def init_program(self):
        pq = ghz(self.qubits)
        ro = pq.declare('ro', memory_size=3)
        assign(ro, self.parties, 'ro')
        self.program = pq

    def check_valid(self):
        return True #TODO

    def run(self):
        if self.check_valid():
            pq = address_qubits(self.program)
            qc = get_qc("5q-qvm")
            result = qc.run(pq)
        else:
            result = None
        self.init_program()
        return result

    def recombine(self, shares):
        pass

def test_hillery1():
    parties = [Hillery1Party(x) for x in 'ABC']
    qc = get_qc("5q-qvm")
    ss = HillerySecretShare1(parties)
    A, B, C = parties
    A.interact(ss)
    B.interact(ss)
    C.interact(ss)
    return ss.run()

if __name__ == '__main__':
    print(test_hillery1())



