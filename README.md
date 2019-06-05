# Quantum Secret Sharing Schemes with PyQuil

## Hillery - Classical
This algorithm allows a party Alice to establish a shared bitstring with Bob and Charlie such that they can only obtain the key if they work together, and neither one can find the key individually. They can use this shared bitstring as however they want, for example as a key for symmetric encryption. This protocol is secure against eavesdroppers. it is implemented implemented in `hillery-classical.py`. 
