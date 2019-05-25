from pyquil.quilatom import QubitPlaceholder, MemoryReference
from consts import *
from pyquil.quil import address_qubits
from pyquil import Program
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE, RX
import numpy as np

def ghz(qubits):
    pq = Program()
    pq += H(qubits[0])
    for i in range(len(qubits)-1):
        pq += CNOT(qubits[i], qubits[i + 1])
    return pq

def assign(things, parties, prop):
    if type(things) == list:
        assert len(things) == len(parties)
    elif type(things) == MemoryReference:
        assert things.declared_size == len(parties)

    for t, p in zip(things, parties):
        setattr(p, prop, t)

def measure_Y(q, reg):
    pq = Program()
    pq += RX(np.pi/2, q)
    pq += MEASURE(q, reg)
    # pq += YINV(q)
    return pq

def measure_X(q, reg):
    pq = Program()
    pq += H(q)
    pq += MEASURE(q, reg)
    pq += H(q)
    return pq

