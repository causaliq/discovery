#
#   Functions to read Bayesys format graph specification files
#

import csv

from causaliq_core.utils import is_valid_path, FileFormatError
from core.graph_new.pdag import PDAG
from core.graph_new.dag import DAG


def read(path, all_nodes=None, strict=True):
    """
        Reads in a graph from a Bayesys format graph specification file

        :param str path: full path name of file
        :param list all_nodes: optional specification of nodes
        :param bool strict: whether strict validation should be applied

        :raises TypeError: if argument types incorrect
        :raises FileNotFoundError: if specified files does not exist
        :raises FileFormatError: if file contents not valid

        :returns DAG/PDAG: DAG or PDAG specified in file
    """
    is_valid_path(path)

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        num_line = 0
        error = ''
        nodes = list(all_nodes) if all_nodes else []
        edges = []
        try:
            for row in reader:
                num_line += 1
                if len(row) != 4:
                    error = ', line {} has not got 4 values'.format(num_line)
                    break
                if num_line == 1:
                    if not strict:  # fix some known content problems
                        row[0] = row[0].replace('Id', "ID")
                        row[1] = row[1].replace('e.1', 'e 1')
                        row[3] = row[3].replace('e.2', 'e 2')
                    if row != ['ID', 'Variable 1', 'Dependency', 'Variable 2']:
                        error = ' has bad header ({})'.format(row)
                        break
                    continue
                if num_line > 1 and row[0] != '{}'.format(num_line - 1):
                    error = ', line {} has bad id'.format(num_line)
                    break

                if all_nodes and (row[1] not in all_nodes
                                  or row[3] not in all_nodes):
                    raise FileFormatError('file {} contains node not in {}'
                                          .format(path, all_nodes))
                if row[1] not in nodes:
                    nodes.append(row[1])
                if row[3] not in nodes:
                    nodes.append(row[3])
                edges.append((row[1], row[2], row[3]))

        except UnicodeDecodeError:
            raise FileFormatError('file {} not in CSV format'.format(path))

        if num_line < 1:
            error = ' is empty'

        if error:
            raise FileFormatError('file {}{}'.format(path, error))
        else:
            graph = PDAG(nodes, edges)
            return graph if not graph.is_DAG() else DAG(nodes, edges)


def write(pdag, path):
    """
        Writes a PDAG to a Bayesys format graph specification file (only
        has details of edges, not unconnected nodes or any parameters)

        :param PDAG pdag: pdag to write to file
        :param str path: full path name of file

        :raises TypeError: if bad arg types
        :raises FileNotFoundError: if path to file does not exist
    """
    if not isinstance(pdag, PDAG) or not isinstance(path, str):
        raise TypeError('bayesys.write() bad arg type')

    with open(path, 'w', encoding='utf-8') as f:
        f.write('ID,Variable 1,Dependency,Variable 2\n')
        num_edges = 0
        for edge, type in pdag.edges.items():
            num_edges += 1
            f.write('{},{},{},{}\n'
                    .format(num_edges, edge[0], type.value[3], edge[1]))
