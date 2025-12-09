
#   Test remove_single_valued() which removes single-valued variables
#   from a BN.

import pytest
from pandas import DataFrame

from causaliq_core.bn import BN
from causaliq_core.graph import DAG
from data.preprocess import remove_single_valued
from data import TESTDATA_DIR
from data.pandas import Pandas
import testdata.example_dags as ex_dag


def test_bn_remove_single_valued_type_error_1():
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    with pytest.raises(TypeError):
        remove_single_valued(bn, )
    with pytest.raises(TypeError):
        remove_single_valued(bn, 52.1)
    with pytest.raises(TypeError):
        remove_single_valued(bn, {'A': ['0'], 'B': ['1']})


def test_bn_remove_single_valued_value_error_1():  # one row only
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    data = DataFrame({'A': ['0'], 'B': ['1'], 'C': ['1']}, dtype='category')
    with pytest.raises(ValueError):
        remove_single_valued(bn, data)


def test_bn_remove_single_valued_value_error_2():  # all vars single-valued
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    data = DataFrame({'A': ['0', '0'], 'B': ['1', '1'], 'C': ['1', '1']},
                     dtype='category')
    with pytest.raises(ValueError):
        remove_single_valued(bn, data)


def test_bn_remove_single_valued_value_error_3():  # one var multi-valued
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    data = DataFrame({'A': ['0', '0'], 'B': ['0', '1'], 'C': ['1', '1']},
                     dtype='category')
    with pytest.raises(ValueError):
        remove_single_valued(bn, data)


def test_bn_remove_single_valued_abc_ok_1():  # no variables need removing
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    data = DataFrame({'A': ['0', '1'], 'B': ['1', '0'], 'C': ['1', '0']},
                     dtype='category')
    new_bn, new_data, removed = remove_single_valued(bn, data)
    assert removed == []
    assert bn == new_bn
    assert not len(new_data.compare(data).columns)


def test_bn_remove_single_valued_abc_ok_2():  # one value needs removing
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    data = DataFrame({'A': ['0', '1'], 'B': ['1', '0'], 'C': ['1', '1']},
                     dtype='category')
    new_bn, new_data, removed = remove_single_valued(bn, data)
    assert removed == ['C']
    expected_data = DataFrame({'A': ['0', '1'], 'B': ['1', '0']},
                              dtype='category')
    assert not len(new_data.compare(expected_data).columns)
    expected_data = Pandas(df=expected_data)
    print(type(expected_data))
    return
    expected_bn = BN.fit(ex_dag.ab(), expected_data)
    assert expected_bn == new_bn


def test_bn_remove_single_valued_abc_ok_3():  # one value needs removing
    bn = BN.read(TESTDATA_DIR + '/discrete/tiny/abc.dsc')
    data = DataFrame({'A': ['0', '0'], 'B': ['1', '0'], 'C': ['1', '0']},
                     dtype='category')
    new_bn, new_data, removed = remove_single_valued(bn, data)
    assert removed == ['A']
    expected_data = DataFrame({'B': ['1', '0'], 'C': ['1', '0']},
                              dtype='category')
    assert not len(new_data.compare(expected_data).columns)
    expected_data = Pandas(df=expected_data)
    expected_bn = BN.fit(DAG(['B', 'C'], [('B', '->', 'C')]), expected_data)
    assert expected_bn == new_bn


def test_bn_remove_single_valued_cancer_ok_1():  # no variables need removing
    bn = BN.read(TESTDATA_DIR + '/discrete/small/cancer.dsc')
    data = bn.generate_cases(100)
    new_bn, new_data, removed = remove_single_valued(bn, data)
    assert removed == []
    assert bn == new_bn
    assert not len(new_data.compare(data).columns)


def test_bn_remove_single_valued_cancer_ok_2():  # Xray need removing
    bn = BN.read(TESTDATA_DIR + '/discrete/small/cancer.dsc')
    data = bn.generate_cases(100).assign(Xray='negative')
    new_bn, new_data, removed = remove_single_valued(bn, data)
    assert removed == ['Xray']
    expected_data = data.drop(labels=['Xray'], axis='columns').copy()
    assert not len(new_data.compare(expected_data).columns)
    expected_data = Pandas(df=expected_data)
    expected_bn = BN.fit(DAG(['Smoker', 'Cancer', 'Pollution', 'Dyspnoea'],
                             [('Smoker', '->', 'Cancer'),
                              ('Pollution', '->', 'Cancer'),
                              ('Cancer', '->', 'Dyspnoea')]),
                         expected_data)
    assert expected_bn == new_bn


def test_bn_remove_single_valued_cancer_ok_3():  # Xray, Smoker need removing
    bn = BN.read(TESTDATA_DIR + '/discrete/small/cancer.dsc')
    data = bn.generate_cases(100).assign(Xray='negative', Smoker='False')
    new_bn, new_data, removed = remove_single_valued(bn, data)
    assert removed == ['Smoker', 'Xray']
    expected_data = data.drop(labels=['Xray', 'Smoker'], axis='columns').copy()
    assert not len(new_data.compare(expected_data).columns)
    expected_data = Pandas(df=expected_data)
    expected_bn = BN.fit(DAG(['Cancer', 'Pollution', 'Dyspnoea'],
                             [('Pollution', '->', 'Cancer'),
                              ('Cancer', '->', 'Dyspnoea')]),
                         expected_data)
    assert expected_bn == new_bn


@pytest.mark.slow
def test_bn_remove_single_valued_pathfinder_1K_ok():  # Pathfinder, 1K rows
    bn = BN.read(TESTDATA_DIR + '/discrete/verylarge/pathfinder.dsc')
    data = bn.generate_cases(1000)
    _, _, removed = remove_single_valued(bn, data)
    assert removed == ['F13', 'F15', 'F27', 'F69', 'F72', 'F75']


@pytest.mark.slow
def test_bn_remove_single_valued_pathfinder_2K_ok():  # Pathfinder, 2K rows
    bn = BN.read(TESTDATA_DIR + '/discrete/verylarge/pathfinder.dsc')
    data = bn.generate_cases(2000)
    _, _, removed = remove_single_valued(bn, data)
    assert removed == ['F15', 'F27', 'F72', 'F75']
