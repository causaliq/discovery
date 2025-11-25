#
#   Classes used across core package
#

from enum import Enum
from numpy import log, log2, log10
from math import floor
from numpy.random import default_rng
from pandas import DataFrame
from pathlib import Path
from json import dump, load
from time import time
from platform import uname
from cpuinfo import get_cpu_info
from psutil import virtual_memory

from data import EXPTS_DIR
from causaliq_core.graph import EdgeType

# BAYESYS_VERSIONS migrated to causaliq_core.graph

# Randomise class migrated to causaliq_core.utils.random


_rng = default_rng(1)  # numpy random number generator

STABLE_RANDOM_FILE = '/stable_random.dat'
_stable_random = None  # sequence of random numbers read from disk file
_stable_random_offset = 0  # shift which allows different sequences of randos


class EnumWithAttrs(Enum):
    """
        Base class for an Enumeration with values exposed as read-only
        attributes.

        Values of this enum should set by e.g. VALUE1 = value1, label1
        This base class has a read-only value and label. Sub-classes can be
        extended to include more attributes by following the pattern for
        label here, and sub-classing the __init__ with more arguments.
    """
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: str, label: str):
        self._label_ = label

    def __str__(self):
        return self.value

    @property
    def label(self):
        return self._label_


# rndsf function migrated to causaliq_core.math

# ln function migrated to causaliq_core.math

# random_generator function migrated to causaliq_core.utils.random
# set_random_seed function migrated to causaliq_core.utils.random
# generate_stable_random function migrated to causaliq_core.utils.random
# stable_random function migrated to causaliq_core.utils.random
# init_stable_random function migrated to causaliq_core.utils.random

# adjmat function migrated to causaliq_core.graph

# environment function migrated to causaliq_core.utils

# RandomIntegers class migrated to causaliq_core.utils.random
