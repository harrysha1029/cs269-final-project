class SecretShare:
    def __init__(self, parties, k=None):
        self.parties = parties
        self.n = len(parties)
        self.k = k

    def __repr__(self):
        return '<{}> object: n={}, k={}'.format(
            type(self).__name__, self.n, self.k)


    def split(self, secret):
        """
        Takes in the secret, and returns
        Return an n-tuple of shares
        """
        pass

    def recombine(self, shares):
        """
        Takes in a k tuple of shares, and returns
        the secret if all k shares are valid
        """
        pass

class Party():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{}> object: name: {}'.format(
            type(self).__name__, self.name)

    def interact(self, state=None):
        pass

