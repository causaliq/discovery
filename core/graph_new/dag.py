#
#   Directed Acyclic Graph (DAG) class
#

from .pdag import PDAG, NotPDAGError


class NotDAGError(Exception):
    """
        Indicates graph is not a DAG when one is expected
    """
    pass


class DAG(PDAG):
    """
        Directed Acyclic Graph (DAG)

        :param list nodes: nodes present in the graph
        :param list edges: edges which define the graph connections as list
                           of tuples: (node1, dependency symbol, node2)

        :ivar list nodes: graph nodes in alphabetical order
        :ivar dict edges: graph edges {(node1, node2): EdgeType}
        :ivar bool is_directed: always True for DAGs
        :ivar dict parents: parents of node {node: [parents]}

        :raises TypeError: if nodes and edges not both lists
        :raises ValueError: node or edge invalid
    """

    def __init__(self, nodes, edges):

        try:
            PDAG.__init__(self, nodes, edges)
        except NotPDAGError:
            raise NotDAGError("graph is not a DAG")

        if not self.is_DAG():
            raise NotDAGError("graph is not a DAG")

    def ordered_nodes(self):
        """
            Generator which returns nodes in a topological order

            :returns str: next node in topological order
        """
        for group in self.partial_order(self.parents, self.nodes):
            for node in sorted(list(group)):
                yield node

    def to_string(self):
        """
            Compact (bnlearn) string representation of DAG e.g. [A][B][C|A:B]

            :returns str: description of graph
        """
        if not self.nodes:
            return ''

        str = ''
        for node in self.nodes:
            str += '[{}'.format(node)
            str += '|' + ':'.join(self.parents[node]) if node in self.parents \
                else ''
            str += ']'
        return str

    def __str__(self):
        """
            A human-readable description of the DAG.

            :returns str: description of DAG
        """
        graph_desc = super().__str__()
        graph_desc = graph_desc.replace('SDG', 'DAG', 1)
        return graph_desc

    @classmethod
    def extendPDAG(cls, pdag):
        """
            Generates a DAG which extends a PDAG
        """
        from .convert import extendPDAG
        return extendPDAG(pdag)