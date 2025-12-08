# Abstract superclass for data objects

from abc import ABC, abstractmethod
from os.path import isfile, isdir
from strenum import StrEnum

from causaliq_core.utils.random import RandomIntegers
from causaliq_core.bn.bnfit import BNFit


TESTDATA_DIR = 'testdata'  # Directory where noisy test data files reside
EXPTS_DIR = 'experiments'  # Directory for experimental data and results


class DatasetType(StrEnum):
    CATEGORICAL = 'categorical'  # all categorical variables
    CONTINUOUS = 'continuous'  # all float variables
    MIXED = 'mixed'  # mixed categorical, float or numeric


class VariableType(StrEnum):
    INT16 = 'int16'
    INT32 = 'int32'
    INT64 = 'int64'
    FLOAT32 = 'float32'
    FLOAT64 = 'float64'
    CATEGORY = 'category'


class Data(BNFit):
    """
        Top level data object that implements BNFit interface.

        :param DataFrame/None df: data supplied as Pandas DataFrame
        :param BN/None bn: data specified as BN (Oracle data)
        :param int/None N: sample size

        :ivar tuple nodes: internal (i.e. original) node names
        :ivar tuple order: order in which nodes should be processed
        :ivar dict ext_to_orig: map from external to original names
        :ivar dict orig_to_ext: map from original to external names
        :ivar int N: current sample size being used by the algorithm
        :ivar dict node_types: node types {n1: t1, n2: ....}
        :ivar DataFrame sample: access to underlying data sample
        :ivar dict node_values: categorical node value counts

        :raises TypeError: if bad types supplied
    """

    elapsed = 0.0

    def __init__(self):
        pass

    def set_order(self, order):
        """
            Sets the process order of the nodes to specified one

            :param tuple order: new process order

            :raises TypeError: for bad argument types
            :raises ValueError: for bad argument values
        """
        if (not isinstance(order, tuple)
                or any(not isinstance(n, str) for n in order)):
            raise TypeError('Data.set_order() bad arg type')

        if set(order) != set(self.ext_to_orig.keys()):
            raise ValueError('Data.set_order() bad arg value')

        self.order = tuple(self.nodes.index(self.ext_to_orig[n])
                           for n in order)
        if self.__class__.__name__ == 'Pandas':
            self._update_sample()

    def get_order(self):
        """
            Gets the current process order.

            :returns tuple: of external names of nodes in process order
        """
        return tuple(self.orig_to_ext[self.nodes[i]] for i in self.order)

    def randomise_order(self, seed):
        """
            Randomises the process order of the nodes to specified one

            :param int seed: randomisation seed

            :raises TypeError: for bad argument types
            :raises ValueError: for bad argument values
        """
        if not isinstance(seed, int):
            raise TypeError('Data.randomise_order() bad arg type')

        if seed < 0:
            raise ValueError('Data.randomise_order() bad arg value')

        self.order = tuple(RandomIntegers(len(self.nodes), seed))
        if self.__class__.__name__ == 'Pandas':
            self._update_sample()

    def _set_dstype(self):
        """
            Determine overall dataset type from individual node types.
        """
        n_floats = sum([1 if v in {'float32', 'float64'} else 0
                        for v in self.node_types.values()])
        n_cats = sum([1 if v == 'category' else 0
                      for v in self.node_types.values()])
        self.dstype = ('continuous' if n_floats == len(self.nodes) else
                       ('categorical' if n_cats == len(self.nodes)
                        else 'mixed'))

    def _generate_random_names(self, seed):

        if seed is None:
            self.ext_to_orig = {n: n for n in self.nodes}
            self.orig_to_ext = {n: n for n in self.nodes}
        else:
            ints = [i for i in RandomIntegers(len(self.nodes), seed)]
            self.ext_to_orig = {'X{:03d}{}'.format(ints[i], n[:6]): n
                                for i, n in enumerate(self.nodes)}
            self.orig_to_ext = {orig: ext
                                for ext, orig in self.ext_to_orig.items()}

    @abstractmethod
    def set_N(self, N, seed=None, random_selection=False):
        """
            Set current working sample size.

            :param int N: current working sample size
            :param int/None seed: seed for row order randomisation if reqd.
            :param bool random_selection: whether rows selected is also
                                          randomised.

            :raises TypeError: if bad argument type
            :raises ValueError: if bad argument value
        """
        pass

    @abstractmethod
    def randomise_names(self, seed):
        """
            Randomises the node names that the learning algorithm uses
            (so sensitivity to these names can be assessed).

            :param int/None seed: randomisation seed (if None, names revert
                                  back to original names)

            :raises TypeError: for bad argument types
            :raises ValueError: for bad argument values
        """
        pass

    @abstractmethod
    def marginals(self, node, parents, values_reqd=False):
        """
            Return marginal counts for a node and its parents.

            :param str node: node for which marginals required.
            :param dict parents: {node: parents} parents of non-orphan nodes
            :param bool values_reqd: whether parent and child values required

            :raises TypeError: for bad argument types

            :returns tuple: of counts, and optionally, values:
                            - ndarray counts: 2D, rows=child, cols=parents
                            - int maxcol: maximum number of parental values
                            - tuple rowval: child values for each row
                            - tuple colval: parent combo (dict) for each col
        """
        pass

    @abstractmethod
    def values(self, nodes):
        """
            Return the (float) values for the specified set of nodes. Suitable
            for passing into e.g. linearRegression fitting function

            :param tuple nodes: nodes for which data required

            :raises TypeError: if bad arg type
            :raises ValueError: if bad arg value

            :returns ndarray: Numpy array array of values, each column for a node
        """
        pass

    @abstractmethod
    def as_df(self):
        """
            Return the data as a Pandas dataframe with current sample size
            and column order.

            :returns DataFrame: data as Pandas
        """
        pass

    # Additional abstract methods required by BNFit interface

    @property
    @abstractmethod
    def nodes(self):
        """
            Return the nodes in the network.

            :returns: nodes in the network
            :rtype: tuple
        """
        pass

    @property
    @abstractmethod
    def sample(self):
        """
            Return the current sample size.

            :returns: current sample size
            :rtype: int
        """
        pass

    @property
    @abstractmethod
    def node_types(self):
        """
            Return the types of all nodes.

            :returns: node types
            :rtype: dict
        """
        pass

    @abstractmethod
    def write(self, path):
        """
            Write the network to a file.

            :param str path: path to write to
        """
        pass