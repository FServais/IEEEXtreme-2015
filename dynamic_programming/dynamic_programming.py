import six
from abc import ABCMeta, abstractmethod


class DPParameters(object):

    """A class for dealing with the parameters of a dynamic programming function
    params: tuple representing a set of parameters
    """
    def __init__(self, params=None):
        self.params = params
        return

    """Set the internal parameters with the given set of parameters
    """
    def set_params(self, params):
        self.params = params

    """Set the internal parameters with the given set of parameters and return the corresponding hash string
    """
    def set_and_hash(self, params):
        self.params = params
        return self.hash()

    """Returns a hash string identifying the set of parameters
    By default, the hash is the paramters joined with commas
    To use another kind of hash, this class should be reimplemented
    """
    def hash(self):
        return ','.join([str(param) for param in self.params]) if self.params is not None else ""


class DPCache(six.with_metaclass(ABCMeta, object)):

    """
    """
    def __init__(self, dp_parameters=None):
        self.save_map = {}
        self.dp_parameters = DPParameters() if dp_parameters is None else dp_parameters

    """Returns the optimal value for the given set of parameters
    If the optimal value was already computed, then the result is retrieved in O(1)
    Otherwise, it is computed by calling optfunc with the set of parameters
    """
    def get(self, params):
        key = self.dp_parameters.set_and_hash(params)

        if key not in self.save_map:
            self.save_map[key] = self.optfunc(params)

        return self.save_map[key]

    """Returns true if the optimal value for the given set of parameters was already computed
    """
    def isset(self, params):
        return self.dp_parameters.set_and_hash(params) in self.save_map

    """ Returns the value of the optimal function for the given parameters
    Must implement the dynamic programming formulation in subclasses of DPCache
    In order to cache the computed results (recursively) the function should get the optimal values for
    subproblems with the function get()
    """
    @abstractmethod
    def optfunc(self, params):
        pass

#
# EXAMPLE
# Finding the maximum sum of an array's elements subset by dynamic programming
#
class OptimalArraySum(DPCache):

    def __init__(self, arr):
        super().__init__()
        self.arr = arr

    """Max sum in [0, j[
    """
    def max_sum_from(self, j):
        return self.get((j,))

    def max_sum(self):
        return self.get((len(self.arr) - 1,))

    def optfunc(self, params):
        import numpy as np
        j = params[0]
        if j == 0:
            return self.arr[j]

        current = self.arr[j]
        recur_sum = self.get((j - 1,))

        return np.max([current, recur_sum, current + recur_sum])
