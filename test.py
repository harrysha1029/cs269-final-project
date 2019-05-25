from pyquil.quilatom import QubitPlaceholder
from pyquil.quil import address_qubits
from pyquil import Program, get_qc
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE, RX
from secret import SecretShare
from pyquil.api import WavefunctionSimulator
from helpers import ghz, measure_X
from consts import *

pq = Program(y_measure_definition, y_inv_definition)
sim = WavefunctionSimulator()
pq += X(0)
pq += YINV(0)
print(pq)
print(sim.wavefunction(pq))

