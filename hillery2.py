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
from helpers import ghz, measure_X, measure_Y, assign
import numpy as np
from consts import *

class Hillery2Party(Party):
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
        # # TEST A, B measure 'y'
        # self.direction = 'x' if self.name == 'C' else 'y'

        # # TEST A, B measure 'x'
        # self.direction = 'x'
        secret_share.program += measure_X(self.qubit, self.ro)
        secret_share.measure_list.append("{} Measured".format(self.name))

class Alice(Hillery2Party):
    def __init__(self, name, secret):
        super().__init__(name)
        assert np.linalg.norm(secret) == 1
        self.secret = secret
        self.secret_qubit = QubitPlaceholder() #TODO


class HillerySecretShare2(SecretShare):
    """The second secret sharing protocol from
    Hillery, 1999"""
    def __init__(self, parties):
        super().__init__(parties)
        self.A, self.B, self.C = self.parties
        self.qubits = [p.qubit for p in parties]
        self.init_program()
        self.qc = get_qc("3q-qvm")
        self.n = self.k = 2

    def init_program(self):
        """Initializes the pyquil program with the ghz
        state. Also resets the measure_list.
        """
        #TODO tensor product
        self.measure_list = []
        pq = ghz(self.qubits)
        ro = pq.declare('ro', memory_size=3)
        assign(ro, self.parties, 'ro')
        self.program = pq
        # TODO measure in bell basis ALICE

    def check_valid(self):
        pass #TODO

    def run(self):
        if self.check_valid():
            pq = address_qubits(self.program)
            result = self.qc.run(pq).flatten()
            # for i, p in enumerate(self.parties):
            #     p.measurements.append(result[i])
            #     p.directions.append(self.measure_list)
        else:
            pass #TODO


def recombine(B, C):
    #TODO
    pass
