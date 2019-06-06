"""
File: hillery2.py
Author: Harry Sha, Katy Woo
Description: Implements the second quantum secret sharing scheme
from Hillery et al. 1999.
"""
from pyquil.quilatom import QubitPlaceholder, MemoryReference
from pyquil.quil import address_qubits, DefGate
from pyquil import Program, get_qc
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE
from secret import SecretShare, Party
from pyquil.api import WavefunctionSimulator
from helpers import ghz, measure_X, measure_Y, assign, measure_Bell, list_to_gate
import numpy as np
from consts import *

sim = WavefunctionSimulator()

class Hillery2Party(Party):
    """ An honest party in the first secret
    sharing protocol.
    """
    def __init__(self, name):
        super().__init__(name)
        self.qubit = QubitPlaceholder()
        self.measurements = []

    def interact(self, secret_share):
        """Interacts with the HillerySecretShare2
        object. In particular, it randomly samples a
        direction in which to measure and announces it
        """
        secret_share.program += measure_X(self.qubit, self.ro)
        secret_share.ready = True


class Alice(Hillery2Party):
    def __init__(self, name, secret):
        super().__init__(name)
        assert np.linalg.norm(secret) == 1
        self.secret = secret
        self.secret_qubit = QubitPlaceholder()


class HillerySecretShare2(SecretShare):
    """The second secret sharing protocol from
    Hillery, 1999"""
    def __init__(self, parties):
        super().__init__(parties)
        self.A, self.B, self.C = self.parties
        self.qubits = [p.qubit for p in parties]
        self.init_program()
        self.qc = get_qc("4q-qvm")
        self.n = self.k = 2
        self.ready = False

    def init_program(self):
        """Initializes the pyquil program with the ghz
        state. Also resets the measure_list.
        """
        pq = ghz(self.qubits)
        ro = pq.declare('ro', memory_size=4)
        assign(ro, self.parties, 'ro')
        self.A.secret_ro = ro[3]
        pq += measure_Bell(self.A.secret_qubit, self.A.qubit, self.A.secret_ro, self.A.ro)
        self.secret_gate = list_to_gate(self.A.secret)
        secret_gate_constructor = self.secret_gate.get_constructor()
        self.program = Program(secret_gate_constructor(self.A.secret_qubit)) +  pq

    def check_valid(self):
        return self.ready

    def create_program(self):
        pq = self.program
        c = self.C.qubit

        p11 = Program().if_then(self.B.ro, Program(Z(c), X(c), Z(c)), Program(X(c), Z(c)))
        p10 = Program().if_then(self.B.ro, Program(I(c)), Program(Z(c)))
        p01 = Program().if_then(self.B.ro, Program(Z(c), X(c)), Program(X(c)))
        p00 = Program().if_then(self.B.ro, Program(Z(c)), Program(I(c)))

        p1 = Program().if_then(self.A.ro, p11, p10)
        p0 = Program().if_then(self.A.ro, p01, p00)
        pq.if_then(self.A.secret_ro, p1, p0)
        self.program = pq

    def run(self, verbose=0):
        if self.check_valid():
            self.create_program()
            pq = address_qubits(self.program, qubit_mapping = {
                self.A.qubit:0,
                self.B.qubit:1,
                self.C.qubit:2,
                self.A.secret_qubit:3
                })
            pq = Program(self.secret_gate) + pq
            if verbose:
                print('The resulting wavefunction is ', sim.wavefunction(pq))
        else:
            print('There was an error in the protocol')
        self.ready = False

if __name__ == '__main__':
    A = Alice('A', (0.6, -0.8j))
    B = Hillery2Party('B')
    C = Hillery2Party('C')
    ss = HillerySecretShare2((A, B, C))
    B.interact(ss)
    ss.run(1)

