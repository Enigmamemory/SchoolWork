class Node:
    def __init__(self, active = None):
        self.active = active
        self.weights = None
        self.pact = None
        self.delta = None

    def retActive(self):
        return self.active

    def retWeights(self):
        return self.weights

    def retPact(self):
        return self.pact

    def retDelta(self):
        return self.delta
    
    def inActive(self, active):
        self.active = active

    def inWeights(self, weights):
        self.weights = weights

    def inPact(self, pact):
        self.pact = pact

    def inDelta(self, delta):
        self.delta = delta
