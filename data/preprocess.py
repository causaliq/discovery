# Data preprocessing utilities for Bayesian Networks

from pandas import DataFrame
from causaliq_core.bn import BN
from causaliq_core.graph import DAG


def remove_single_valued(bn, data):
    """
    Remove nodes from BN that just contain a single value in data.
    This can be useful when syntheticaly generated data is used for
    testing or structure learning as it may have variables which only
    contain one value.

    :param BN bn: Bayesian Network to modify
    :param DataFrame data: data for BN which may contain single-valued
                           or zero-valued variables which should be
                           removed.

    :raises TypeError: if data is not a Pandas dataframe.
    :raises ValueError: if less than 2 multi-valued variables

    :returns tuple: (BN, DataFrame, list) BN and data with offending
                    variables removed, and list of removed variables.
    """
    if not isinstance(data, DataFrame):
        raise TypeError("remove_single_valued_variables() bad arg type")

    remove = sorted(
        [col for col, count in data.nunique().items() if count < 2]
    )
    if len(data.columns) - len(remove) < 2:
        raise ValueError("remove_single_valued_variables() - <2 multi-valued")

    if not len(remove):  # nothing to do
        return (bn, data, remove)

    # Drop single-valued variables from nodes, edges and data

    data = data.drop(labels=remove, axis="columns").astype("category")
    nodes = list(set(bn.dag.nodes) - set(remove))
    edges = [
        (e[0], t.value[3], e[1])
        for e, t in bn.dag.edges.items()
        if e[0] not in remove and e[1] not in remove
    ]

    # Create new BN with filtered data using legacy data adapter
    from data.pandas import Pandas
    data_adapter = Pandas(df=data)
    return (BN.fit(DAG(nodes, edges), data_adapter), data_adapter.sample, remove)