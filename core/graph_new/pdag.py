#
#   Partially Directed Acyclic Graph (PDAG) class
#

from causaliq_core.graph import EdgeType
from .sdg import SDG


class NotPDAGError(Exception):
    """
        Indicates graph is not a PDAG when one is expected
    """
    pass


class PDAG(SDG):
    """
        Partially directed acyclic graph (PDAG)

        :param list nodes: nodes present in the graph
        :param list edges: edges which define the graph connections as list
                           of tuples: (node1, dependency symbol, node2)

        :ivar list nodes: graph nodes in alphabetical order
        :ivar dict edges: graph edges {(node1, node2): EdgeType}
        :ivar bool is_directed: graph only has directed (causal) edges
        :ivar dict parents: parents of node {node: [parents]}

        :raises TypeError: if nodes and edges not both lists
        :raises ValueError: node or edge invalid
    """
    def __init__(self, nodes, edges):

        SDG.__init__(self, nodes, edges)

        if not self.is_PDAG():
            raise NotPDAGError("graph is not a PDAG")

    def edge_reversible(self, edge):
        """
            Returns whether specified edge is in CPDAG and is reversible

            :param tuple edge: edge to examine, (node1, node2)

            :returns bool: whether present and reversible, or not
        """
        if not isinstance(edge, tuple) or not len(edge) == 2 or \
                not isinstance(edge[0], str) or not isinstance(edge[1], str):
            raise TypeError('PDAG.edge_reversible() bad arg type')

        e = (min(edge), max(edge))
        return e in self.edges and self.edges[e] == EdgeType.UNDIRECTED

    def is_cpdag(self):
        """
            Whether the PDAG is a Completed PDAG (CPDAG)

            :raises ValueError: if PDAG is not extendable

            return bool: True if CPDAG, otherwise False
        """
        from .convert import pdag_to_cpdag
        return pdag_to_cpdag(self) == self

    @classmethod
    def dag_to_pdag(cls, dag):
        """
            Generates PDAG representing equivalence class DAG belongs to.
        """
        from .convert import dag_to_pdag
        return dag_to_pdag(dag)

    @classmethod
    def pdag_to_cpdag(cls, pdag):
        """
            Generates a completed PDAG (CPDAG) from supplied PDAG
        """
        from .convert import pdag_to_cpdag
        return pdag_to_cpdag(pdag)