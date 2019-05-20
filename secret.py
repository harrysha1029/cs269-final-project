class SecretShare:
    def __init__(self, n, k):
        self.n, self.k = n, k

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

