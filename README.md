# Quantum Secret Sharing Schemes with PyQuil

Below are highlevel descriptions of the algorithms implemented here. For an explanation on the theory behind this project, please refer to the wiki <https://github.com/harrysha1029/cs269-final-project/wiki>. For examples on the usage of the code, please refer to the jupyter notebook, `Examples.ipynb`. 

To get started, clone the repository, and install requirements with the following 
```
git clone https://github.com/harrysha1029/cs269-final-project.git
cd cs269-final-project
pip install -r requirements.txt
```

Note that the [Forest SDK](http://docs.rigetti.com/en/stable/) is also required in order for the code to run.

## Hillery - Classical
This algorithm allows a party Alice to establish a shared bitstring with Bob and Charlie such that they can only obtain the key if they work together, and neither one can find the key individually. They can use this shared bitstring as however they want, for example as a key for symmetric encryption. This protocol is secure against eavesdroppers. it is implemented in `hillery_classical.py`.

## Hillery - Quantum
This algorithm allows a party Alice to share a quantum state between two Bob and Charlie, such that they can only recover the state if they cooperate. This is implemented in `hillery_quantum.py`

## Cleve - Multiparty
This algorithm shares a secret quantum state between n parties such that at least k of them are required to recover the secret state. It is implemented in `cleve.py`
