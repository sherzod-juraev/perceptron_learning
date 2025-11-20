from numpy import ndarray, float64, dot, unique
from .preprocessing import preprocessing
from numpy.random import uniform


class Perceptron:
    def __init__(self, learning_rate: float = .1, n_iter: int = 10_000, /):

        self.eta = learning_rate
        self.n_iter = n_iter
        self.weights = None
        self.bias = round(uniform(-.01, .01).item(), 4)
        self.classes = None

    def fit(self, X: ndarray, Y: ndarray, /) -> bool:

        preprocessing(X, Y)
        self.classes = unique(Y)
        self.initialize_weight(X.shape[1])
        length = X.shape[0]
        for i in range(self.n_iter):
            result = True
            for j in range(length):
                z = self.predict(X[j])
                if Y[j] != z:
                    self.update_features(X[j], Y[j]-z)
                    result = False
            if result:
                return True
        return False

    def initialize_weight(self, array_size: int, /):

        self.weights = uniform(-.01, .01, size=array_size)

    def net_input(self, X: ndarray, /) -> float64:

        z = dot(X, self.weights) + self.bias
        return z

    def predict(self, X: ndarray, /) -> int:

        z = self.classes[0] if self.net_input(X) >= 0 else self.classes[1]
        return int(z)

    def update_features(self, X: ndarray, error: int, /):

        self.weights += self.eta * error * X
        self.bias += self.eta * error