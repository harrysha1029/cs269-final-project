from pyquil.quilatom import QubitPlaceholder
from pyquil.quil import address_qubits
from pyquil import Program, get_qc
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE, RX
from secret import SecretShare
from pyquil.api import WavefunctionSimulator
from helpers import ghz, measure_X, measure_Bell, measure_Y, list_to_gate
from consts import *
from grove.alpha.arbitrary_state.arbitrary_state import create_arbitrary_state
from sympy import sieve
import itertools

K = 2
M = 3

# finding the base field prime
def get_q(m, s):
    return sieve.primerange(max(m, s), 2*max(m, s)).__next__()

# we use distinct points x_i = i  in F_q for simplicity

# creating and evaluating a polynomial
def poly_vect_gen(c, q, m):
    vect = [0]*m
    for i in range(len(c)):
        for j in range(len(vect)):
            vect[j] = (vect[j] + c[i]*(j**i)) % q
    return vect

# vector to number using base q representation
def vect_to_num(vect, q):
    num = 0
    for i in range(len(vect)):
        num = num + vect[i]*(q**i)
    return num

# create the polynomial state for a vector |a>
def create_poly_state(a, q, m):
    sum_state = [0]*(q**m)
    tuples = itertools.product(range(q), repeat=K-1)
    for t in tuples:
        t = list(t)
        t.append(a)
        n = vect_to_num(poly_vect_gen(t, q, m), q)
        sum_state[n] = sum_state[n]+1
    return sum_state

def sum_state_to_quantum(sum_state):
    ss = np.array(sum_state)
    print(ss)
    normalized = ss/np.linalg.norm(ss)
    return create_arbitrary_state(normalized)


sum_state = create_poly_state(2, 1, 3, M)

sim = WavefunctionSimulator()
print(sim.wavefunction(sum_state_to_quantum(sum_state)))




vec = np.array([1, 2, 3j])
vec = vec/np.linalg.norm(vec)
print(vec)


qubits = QubitPlaceholder.register(4)
A, B, C, secret = qubits
s_gate = list_to_gate([0.6, -0.8j])
pq = ghz(qubits[:3])

