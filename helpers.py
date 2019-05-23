from pyquil.quilatom import QubitPlaceholder
from pyquil.quil import address_qubits
from pyquil import Program
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE

def ghz(qubits):
    pq = Program()
    pq += H(qubits[0])
    for i in range(len(qubits)-1):
        pq += CNOT(qubits[i], qubits[i + 1])
    return pq

def measure_X(q, ro, ro_ind):
    pq = Program()
    pq += H(q)
    pq += MEASURE(q, ro[ro_ind])
    pq += H(q)
    return pq
