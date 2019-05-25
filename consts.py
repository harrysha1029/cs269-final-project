import numpy as np
from pyquil.quil import DefGate

num2direction = {0:'x', 1:'y'}

# m = np.array([[1, -1j],[1, 1j]])/np.sqrt(2)
# m_inv = np.linalg.inv(m)
# y_measure_definition = DefGate('YMEASURE', m)
# YMEASURE = y_measure_definition.get_constructor()
# y_inv_definition = DefGate('YINV', m_inv)
# YINV = y_inv_definition.get_constructor()
