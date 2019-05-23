from pyquil.quilatom import QubitPlaceholder
from pyquil.quil import address_qubits
from pyquil import Program, get_qc
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE
from secret import SecretShare
from pyquil.api import WavefunctionSimulator
from helpers import ghz, measure_X

N = 3

class HillerySecretShare1(SecretShare):
    """The first secret sharing protocol from
    Hillery, 1999"""
    def __init__(self):
        self.n = self.k = 2

    def split(self, secret):
        pass

    def recombine(self, shares):
        pass

if __name__ == '__main__':
    qubits = QubitPlaceholder.register(N)
    x = ghz(qubits)
    ro = x.declare('ro')
    x += measure_X(qubits[0], ro, 0)

    x = address_qubits(x)
    qc = get_qc("5q-qvm")
    print(qc.run(x))

    wfn = WavefunctionSimulator().wavefunction(x)
    print(wfn)

