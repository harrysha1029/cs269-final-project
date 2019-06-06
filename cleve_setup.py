import itertools
from collections import defaultdict
from pyquil.quilatom import QubitPlaceholder
from pyquil.quil import address_qubits
from pyquil import Program, get_qc
from pyquil.gates import X, I, Y, Z, H, CNOT, MEASURE, RX
from pyquil.api import WavefunctionSimulator
from grove.alpha.arbitrary_state.arbitrary_state import create_arbitrary_state
from sympy import sieve
from sympy import Matrix
import numpy as np

def num2bin(n, b_len):
    """ Convert an integer n to its
    binary representation padded to
    have b_len binary digits
    """
    f_string = '{0:0'+ str(b_len) + 'b}'
    return f_string.format(n)

def long_state_from_vec(vec, q):
    """
    Converts the state |2, 3, 1, 5> to
    its representation in binary. q
    is the largest possible basis state
    """
    b_len = int(np.log2(q)) + 1
    binary_rep = ''.join([num2bin(v, b_len) for v in vec])
    return binary_rep

# creating and evaluating a polynomial
def poly_vect_gen(c, q, m):
    vect = [0]*m
    for i in range(len(c)):
        for j in range(len(vect)):
            vect[j] = (vect[j] + c[i]*((j+1)**i)) % q
    return vect

# create the polynomial state for a vector |a>
def create_poly_state(states, alphas, q, m, k):
    """ Set up quantum state by summing over polynomials
    Returns sum_state, which is the constructed quantum
    state, and count, which is a dictionary mapping
    states to weights.
    """
    count = defaultdict(int)
    tuples = list(itertools.product(range(q), repeat=k-1))
    for a, alpha in zip(states, alphas):
        for t in tuples:
            t = list(t)
            t.append(a)
            p_c = poly_vect_gen(t, q, m)
            state = long_state_from_vec(p_c, q)
            count[state] += alpha

    max_num = 2**len(state)-1
    coeff_vec = np.zeros(max_num).astype(np.complex)
    count_ind = {int(k, 2): v for k, v in count.items()}
    for k ,v in count_ind.items():
        coeff_vec[k] = v

    normalized = coeff_vec/np.linalg.norm(coeff_vec)
    sum_state = None #create_arbitrary_state(normalized)

    return sum_state, count

