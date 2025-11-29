#
#   Graph conversion operations
#

def dag_to_pdag(dag):
    """
        Generates PDAG representing equivalence class DAG belongs to.

        Uses the algorithm in "A Transformational Characterization of
        Equivalent Bayesian Network Structures", Chickering, 1995. Step
        numbers in comments refer to algorithm step numbers in paper.

        :param DAG dag: DAG whose PDAG is required.

        :raises TypeError: if dag is not of type DAG

        :returns PDAG: PDAG for equivalence class that dag belongs to
    """
    # Import here to avoid circular imports
    from .dag import DAG
    from .pdag import PDAG

    def _process_x(x, y, edges):  # process incoming edges to x

        if not len(parents[x]):  # nothing to do if no parents of x
            # print('#5 no incoming to {} so no op'.format(x))
            return (edges, False)

        for w in parents[x]:  # Step 5 - Loop over inbound edges to x ...
            if (w, '->', x) in edges:  # ... that are compelled
                if w not in parents[y]:

                    # Step 6 - if w is not a parent of y then label all
                    #          inbound to y as compelled and exit

                    # print(('#6 {}->{} compelled, not parent of {}' +
                    #        ', so compel all inbound to {}')
                    #       .format(w, x, y, y))
                    return ([(e[0], '->', e[2]) if e[2] == y else e
                             for e in edges], True)
                else:

                    # Step 7 - if w is parent of y then compel w -> y

                    # print('#7 {}->{} so compel it'.format(w, y))
                    edges = [(e[0], '->', e[2]) if e[0] == w and e[2] == y
                             else e for e in edges]
        return (edges, False)

    def _process_y(x, y, edges):  # process incoming edges to y

        # Step 8 - if there is an edge z -> y where z is not x or a parent
        #          of x, label x -> y all unknown inbound to y as compelled

        for z in parents[y]:
            if z != x and z not in parents[x]:
                # print('#8 {} not -> {} so compel all inbound to {}'
                #       .format(z, x, y))
                return [(e[0], '->', e[2]) if (e[0] == x or e[1] == '?')
                        and e[2] == y else e for e in edges]

        # Step 9 - set x -> y and unknown inbound arcs to y to reversible

        # print('#9 set inbound to {} as "-"'.format(y))
        return [(e[0], '-', e[2]) if (e[0] == x or e[1] == '?')
                and e[2] == y else e for e in edges]

    if not isinstance(dag, DAG):
        raise TypeError("dag arg in dag_to_pdag not a DAG")

    nodes = [n for n in dag.ordered_nodes()]  # nodes in topological order
    parents = {n: [p for p in nodes if p in  # node parents in topo order
               (dag.parents[n] if n in dag.parents else [])]
               for n in nodes}
    edges = [(p, '?', n) for n in reversed(nodes) for p in parents[n]]
    edges = [e for e in reversed(edges)]
    # print('dag_to_pdag: reversed ordered edges are: {}'.format(edges))

    while any([t == '?'for (_, t, _) in edges]):  # 3 some edges unknown
        for i, (x, _, y) in enumerate(edges):
            if edges[i][1] != '?':  # 4 dynamic lowest unknown edge
                continue
            # print('#4 processing {} ? {} edge in {}'.format(x, y, edges))

            edges, restart = _process_x(x, y, edges)  # 5-7 incoming to x
            if restart:
                break

            edges = _process_y(x, y, edges)  # 8&9, edges incoming to y

    return PDAG(dag.nodes, edges)


def pdag_to_cpdag(pdag):
    """
        Generates a completed PDAG (CPDAG) from supplied PDAG

        :param PDAG pdag: PDAG to be completed

        :raises TypeError: if pdag is not of type PDAG
        :raises ValueError: if pdag is non-extendable

        :returns PDAG/None: CPDAG corresponding to pdag
    """
    # Import here to avoid circular imports
    from .dag import DAG
    from .pdag import PDAG

    dag = extend_pdag(pdag)
    return dag_to_pdag(dag) if dag is not None else None


def extend_pdag(pdag):
    """
        Generates a DAG which extends a PDAG (i.e. is a member of the
        equivalence class the PDAG represents)

        Uses the algorithm in "A simple algorithm to construct a
        consistent extension of a partially oriented graph",
        Dor and Tarsi, 1992

        :param PDAG pdag: PDAG from which DAG derived

        :raises TypeError: if pdag is not of type PDAG
        :raises ValueError: if pdag is not extendable (example is
                            an undirected square PDAG)

        :returns DAG: extension of pdag
    """
    # Import here to avoid circular imports  
    from .dag import DAG
    from .pdag import PDAG
    from causaliq_core.graph import EdgeType

    def _adj(n, s, pc=True):
        et = [EdgeType.UNDIRECTED, EdgeType.DIRECTED] if pc \
            else [EdgeType.UNDIRECTED]
        return {e[0] if e[1] == n else e[1] for e, t in s.edges.items()
                if (e[0] == n or e[1] == n) and t in et}

    def _valid_x(s):

        # Looking for a node in s which satisfies properties a and b

        for x in s.nodes:

            # a. x is a sink node, i.e. no outbound directed edges

            is_sink = not any([e[0] == x and t == EdgeType.DIRECTED
                               for e, t in s.edges.items()])
            if not is_sink:
                continue
            # print('{} is{} a sink'.format(x, '' if is_sink else ' not'))

            # b. - all nodes, y, attached to n by an undirected edge
            #      are adjacent to all neighbours (nb) of node n

            cond_b = True
            adj_x = _adj(x, s)
            # print('Neighbours of {} are {}'.f#ormat(x, adj_x))
            # print('Peers of {} are {}'.format(x, _adj(x, s, False)))
            for y in _adj(x, s, False):
                adj_y = _adj(y, s) - {x}
                # print('{} are adjacent to {}'.format(adj_y, y))
                # print('{} is a subset of {}: {}'
                #       .format(adj_x - {y}, adj_y,
                #               (adj_x - {y}).issubset(adj_y)))
                if not (adj_x - {y}).issubset(adj_y):
                    cond_b = False
                    break

            if cond_b:  # found node n that has properties a and b
                return x

        return None  # no node found that has properties a and b

    if not isinstance(pdag, PDAG):
        raise TypeError("pdag arg in extend_pdag not a PDAG")

    if pdag.is_directed:  # if already directed just return as DAG class
        return DAG(pdag.nodes, [(e[0], '->', e[1])
                                for e in pdag.edges.keys()])

    # Clone pdag as dag. The DAG will be created in "dag", matching G' in
    # paper, "pdag" will act as graph A in the paper

    dag = PDAG(pdag.nodes, [(e[0], '->' if t == EdgeType.DIRECTED else '-',
                             e[1]) for e, t in pdag.edges.items()])

    while len(pdag.edges):
        x = _valid_x(pdag)
        # print("Processing eligible node is {}".format(x))
        if x is None:  # means pdag is not extendable
            raise ValueError('pdag is not extendable')

        # orientate all edges incident to x in pdag to go into x in dag

        edges = [(e[0] if e[1] == x else e[1], '->', x)
                 if (e[0] == x or e[1] == x) and e in pdag.edges else
                 # if (e[0] == x or e[1] == x) else
                 (e[0], '->' if t == EdgeType.DIRECTED else '-', e[1])
                 for e, t in dag.edges.items()]
        dag = PDAG(dag.nodes, edges)
        # print('DAG is:\n{}'.format(dag))

        # remove x and its incident edges from pdag for next iteration

        nodes = list(set(pdag.nodes) - {x})
        edges = [(e[0], '->' if t == EdgeType.DIRECTED else '-', e[1])
                 for e, t in pdag.edges.items() if e[0] != x and e[1] != x]
        pdag = PDAG(nodes, edges)
        # print('PDAG is:\n{}\n\n'.format(pdag))

    # return dag as DAG object

    return DAG(dag.nodes, [(e[0], '->' if t == EdgeType.DIRECTED else '?',
                            e[1]) for e, t in dag.edges.items()])