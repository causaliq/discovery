#
#   Simple Directed Graph (SDG) base class
#

from numpy import zeros
from pandas import DataFrame

from causaliq_core.graph import EdgeType


class SDG():
    """
        Base class for simple dependency graphs (one edge between vertices)

        :param list nodes: nodes present in the graph
        :param list edges: edges which define the graph connections as list
                           of tuples: (node1, dependency symbol, node2)

        :ivar list nodes: graph nodes in alphabetical order
        :ivar dict edges: graph edges {(node1, node2): EdgeType}
        :ivar bool is_directed: graph only has directed (causal) edges
        :ivar bool is_partially_directed: graph is partially directed
        :ivar dict parents: parents of node {node: [parents]}
        :ivar bool has_directed_cycles: contains any directed cycles

        :raises TypeError: if nodes and edges not both lists
        :raises ValueError: node or edge invalid
    """

    def __init__(self, nodes, edges):
        """
            Constructor
        """

        if type(nodes) is not list or type(edges) is not list:
            raise TypeError('graph edges and nodes not both lists')

        # Validate nodes specified

        self.nodes = []
        for node in nodes:
            if type(node) is not str:
                raise TypeError('graph has non-string node name')
            if not node:
                raise ValueError('graph has empty node name')
            if node in self.nodes:
                raise ValueError('graph has duplicate node names')
            self.nodes.append(node)
        self.nodes.sort()

        # Validate edges specified

        self.edges = {}
        edge_types = {e.value[3]: e for e in EdgeType}
        self.is_directed = True
        self.is_partially_directed = True
        self.parents = {}
        self.has_directed_cycles = False

        for edge in edges:
            if type(edge) is not tuple or len(edge) != 3:
                raise TypeError('graph has non-triple edge')
            for part in edge:
                if type(part) is not str:
                    raise TypeError('graph has non-string edge triple')
            if edge[0] == edge[2]:
                raise ValueError('graph has cyclic edge')
            if edge[1] not in edge_types:
                raise TypeError('graph edge has unknown type symbol: "{}"'
                                .format(edge[1]))
            if edge[0] not in self.nodes or edge[2] not in self.nodes:
                raise ValueError('graph edge has unknown node')
            if (edge[0], edge[2]) in self.edges or \
                    (edge[2], edge[0]) in self.edges:
                raise ValueError('graph has duplicate edges')

            # Check if graph directed or partially directed
            edge_type = edge_types[edge[1]]
            if edge_type != EdgeType.DIRECTED:
                self.is_directed = False
                if edge_type != EdgeType.UNDIRECTED:
                    self.is_partially_directed = False

            if edge_type == EdgeType.DIRECTED:

                # collect parents for directional links

                if edge[2] in self.parents:
                    self.parents[edge[2]].append(edge[0])
                else:
                    self.parents[edge[2]] = [edge[0]]

            elif edge_type in (EdgeType.UNDIRECTED, EdgeType.BIDIRECTED,
                               EdgeType.NONDIRECTED) and edge[0] > edge[2]:

                # ensure nodes in alphabetical order for non-directional edges

                edge = (edge[2], edge[1], edge[0])

            # parents held in alphabetical order

            self.parents = {k: sorted(v) for k, v in self.parents.items()}

            # store the edge in dictionary {(node1, node2): edge_type}

            self.edges[(edge[0], edge[2])] = edge_type

            # see whether has directed cycles

            self.has_directed_cycles = True if \
                self.partial_order(self.parents, self.nodes) is None else False

    def rename(self, name_map):
        """
            Nodes renamed in place according to name map.

            :param dict name_map: name mapping {name: new name}
                                  - must have mapping for every node

            :raises TypeError: with bad arg type
            :raises ValueError: with bad arg values e.g. unknown node names
        """
        if (not isinstance(name_map, dict)
            or not all([isinstance(k, str) and isinstance(v, str)
                        for k, v in name_map.items()])):
            raise TypeError('SDG.rename() bad arg types')

        if set(name_map.keys()) != set(self.nodes):
            raise ValueError('SDG.raname() bad arg values')

        # Change node names and node names in edges

        nodes = [name_map[n] if n in name_map else n for n in self.nodes]
        edges = [((name_map[e[0]] if e[0] in name_map else e[0]),
                  t.value[3],
                  (name_map[e[1]] if e[1] in name_map else e[1]))
                 for e, t in self.edges.items()]

        # Re-instantiate object with new names

        self = self.__init__(nodes, edges)

    @classmethod
    def partial_order(self, parents, nodes=None, new_arc=None):
        """
            Return partial topological ordering for the directed part of a
            graph which is specified by list of parents for each node.

            :param dict parents: parents of each node {node: [parents]}
            :param list/None nodes: optional complete list of nodes including
                                    parentless ones for use if parents argument
                                    doesn't include them already.
            :param tuple new_arc: a new arc (n1, n2) to be added before order
                                  is evaluated. If the opposing arc is implied
                                  in parents then it is removed so that arc
                                  reversal is also supported. This argument
                                  facilitates seeing whether an arc addition or
                                  reversal would create a cycle

            :returns list/None: nodes in a partial topological order as list of
                                sets or None if there is no ordering which
                                means the graph is cyclic
        """
        if not isinstance(parents, dict) \
                or (nodes is not None and not isinstance(nodes, list)
                    and not isinstance(nodes, set)):
            raise TypeError('DAG.partial_order bad arg type')

        parents_copy = {n: set(p) for n, p in parents.items()}
        if nodes is not None:
            parents_copy.update({n: set() for n in nodes if n not in parents})
        if new_arc is not None:
            parents_copy[new_arc[0]] = parents_copy[new_arc[0]] - {new_arc[1]}
            parents_copy[new_arc[1]] = parents_copy[new_arc[1]] | {new_arc[0]}

        order = []
        while len(parents_copy):
            roots = {n for n in parents_copy if not parents_copy[n]}
            if not len(roots):
                return None
            order.append(roots)
            for root in roots:
                parents_copy.pop(root)
            for node, parents in parents_copy.items():
                parents_copy[node].difference_update(roots)

        return order

    def is_DAG(self):
        """
            Returns whether graph is a Directed Acyclic Graph (DAG)

            :returns bool: whether graph is a DAG
        """
        return self.is_directed and self.has_directed_cycles is False

    def is_PDAG(self):
        """
            Returns whether graph is a Partially Directed Acyclic Graph (PDAG)

            :returns bool: whether graph is a PDAG
        """
        if self.is_directed:
            return self.is_DAG()

        if not self.is_partially_directed:
            return False

        # Check if there are any cycles in directed part of graph

        arcs = [(a[0], '->', a[1]) for a, t in self.edges.items()
                if t == EdgeType.DIRECTED]
        return not SDG(self.nodes, arcs).has_directed_cycles

    def undirected_trees(self):
        """
            Return undirected trees present in graph

            :returns list: of trees, each tree a set of tuples representing
                           edges in tree (n1, n2) or a single isolated node
                           (n1, None)
        """
        trees = []
        edges = {(e[0], e[1]) if e[1] > e[0] else (e[1], e[0])
                 for e in self.edges.keys()}
        isolated = set(self.nodes)
        while len(edges):
            tree = {list(edges)[0]}
            t_nodes = {list(tree)[0][0], list(tree)[0][1]}
            for edge in edges:
                if ((edge[0] in t_nodes and edge[1] not in t_nodes) or
                        (edge[1] in t_nodes and edge[0] not in t_nodes)):
                    t_nodes = t_nodes | {edge[0], edge[1]}
                    tree = tree | {edge}
            edges = edges - tree
            isolated = isolated - t_nodes
            trees.append(tree)
        trees.extend([{(n, None)} for n in isolated])
        return trees

    def components(self):
        """
            Return components present in graph. Uses tree search algorithm
            to span the undirected graph to identify nodes in individual
            trees which are the spanning tree of each component.

            :returns list: of lists, each a list of sorted nodes in component
        """
        components = []
        edges = {(e[0], e[1]) if e[1] > e[0] else (e[1], e[0])
                 for e in self.edges.keys()}  # skeleton of graph
        nodes = set(self.nodes)  # nodes yet to be included in components

        while len(nodes):
            c_nodes = {list(nodes)[0]}  # put 1st arbitrary node in component
            growing = True
            while growing:
                growing = False
                for edge in edges:  # look for edges across component boundary
                    if ((edge[0] in c_nodes and edge[1] not in c_nodes) or
                            (edge[1] in c_nodes and edge[0] not in c_nodes)):
                        c_nodes = c_nodes | {edge[0], edge[1]}
                        growing = True

            # component identified, remove its nodes from consideration

            nodes = nodes - c_nodes
            components.append(sorted(c_nodes))

        return sorted(components)

    def number_components(self):
        """
            Return number of components (including unconnected nodes) in graph

            :returns int: number of components
        """
        return len(self.components())

    def to_adjmat(self):
        """
            Returns an adjacency matrix representation of the graph

            :returns numpy.array: adjacency matrix
        """
        size = len(self.nodes)
        adjmat = zeros(shape=(size, size), dtype='int8')
        adjmat = DataFrame(adjmat, columns=self.nodes)
        adjmat[''] = self.nodes
        adjmat.set_index('', inplace=True)
        for nodes, type in self.edges.items():
            # print('{}: {}'.format(nodes, type.value[0]))
            adjmat.loc[nodes[0], nodes[1]] = type.value[0]

        return adjmat

    def __str__(self):
        """
            A human-readable description of the graph

            :returns str: description of graph
        """
        if not self.nodes:
            return 'Empty graph'

        number_components = self.number_components()
        kind = 'DAG' if self.is_directed else \
            ('PDAG' if self.is_partially_directed else 'SDG')
        desc = '{} ({}), {} node'.format(kind, type(self), len(self.nodes)) + \
            ('' if len(self.nodes) == 1 else 's') +\
            ', {} edge'.format(len(self.edges)) + \
            ('' if len(self.edges) == 1 else 's') + \
            ' and {} component'.format(number_components) + \
            ('' if number_components == 1 else 's')

        for node in self.nodes:
            children = [t.value[3] + str(e[1]) for e, t
                        in self.edges.items() if e[0] == node]
            desc += '\n{}: {}'.format(node, ' '.join(children))
        return desc

    def __eq__(self, other):
        """
            Test if graph is identical to this one

            :param Graph other: graph to compare with self

            :returns bool: True if other is identical to self
        """
        return isinstance(other, SDG) \
            and self.nodes == other.nodes and self.edges == other.edges