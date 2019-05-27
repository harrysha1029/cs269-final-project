import numpy as np
from pyquil.quil import DefGate

num2direction = {0:'x', 1:'y'}
VALID_DIRECTIONS = [
        (('A', 'x'), ('B', 'x'), ('C', 'x')),
        (('A', 'y'), ('B', 'y'), ('C', 'x')),
        (('A', 'x'), ('B', 'y'), ('C', 'y')),
        (('A', 'y'), ('B', 'x'), ('C', 'y'))
        ]
B_IS_SAME_AS_A = {
        ('x', 'x', 'x', 0): True,
        ('x', 'x', 'x', 1): False,
        ('x', 'y', 'y', 0): False,
        ('x', 'y', 'y', 1): True,
        ('y', 'x', 'y', 0): False,
        ('y', 'x', 'y', 1): True,
        ('y', 'y', 'x', 0): False,
        ('y', 'y', 'x', 1): True,
        }

# m = np.array([[1, -1j],[1, 1j]])/np.sqrt(2)
# m_inv = np.linalg.inv(m)
# y_measure_definition = DefGate('YMEASURE', m)
# YMEASURE = y_measure_definition.get_constructor()
# y_inv_definition = DefGate('YINV', m_inv)
# YINV = y_inv_definition.get_constructor()
