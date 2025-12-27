
#   Test the method to compare Traces

import pytest

from learn.trace import Trace
from causaliq_analysis.graph import GraphAction
from causaliq_analysis.graph import GraphActionDetail


def test_trace_diffs_type_error_1():  # bad arg type for diffs_from
    with pytest.raises(TypeError):
        Trace().diffs_from()
    with pytest.raises(TypeError):
        Trace().diffs_from(-400.001)
    with pytest.raises(TypeError):
        Trace().diffs_from(True)


def test_trace_diffs_value_error_1():  # both traces empty
    with pytest.raises(ValueError):
        Trace().diffs_from(Trace())


def test_trace_diffs_value_error_2():  # trace empty
    trace = Trace()
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_3():  # reference empty
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace()
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_4():  # both traces too short
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_5():  # trace doesn't start with init
    trace = Trace().add(GraphAction.STOP, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_6():  # trace doesn't start with init
    trace = Trace().add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_7():  # ref doesn't start with init
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.STOP, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_8():  # ref doesn't start with init
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_9():  # trace doesn't end with stop
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.INIT, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_10():  # trace doesn't end with stop
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'C'),
                                       GraphActionDetail.DELTA: 1.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.INIT, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_11():  # ref doesn't end with stop
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.INIT, {GraphActionDetail.DELTA: 10.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_value_error_12():  # ref doesn't end with stop
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.INIT, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'C'),
                                     GraphActionDetail.DELTA: 1.0})
    with pytest.raises(ValueError):
        trace.diffs_from(ref)


def test_trace_diffs_same_ok_1():  # two entries identical
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_same_ok_2():  # three entries identical
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_same_ok_3():  # three identical entries
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_same_ok_4():  # seven identical entries
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 3.0}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('C', 'D'),
                                       GraphActionDetail.DELTA: 2.0}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.5}) \
                   .add(GraphAction.DEL, {GraphActionDetail.ARC: ('C', 'D'),
                                       GraphActionDetail.DELTA: 0.1}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -3.52345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 3.0}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('C', 'D'),
                                     GraphActionDetail.DELTA: 2.0}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.5}) \
                 .add(GraphAction.DEL, {GraphActionDetail.ARC: ('C', 'D'),
                                     GraphActionDetail.DELTA: 0.1}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -3.52345678})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_same_ok_5():  # small score differences
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0001})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: 0.00003}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: 10.0})

    diffs = trace.diffs_from(ref)  # strict comparisons
    assert diffs[0] == {('init', 'score'): {None: (0, 0)},
                        ('stop', 'score'): {None: (1, 1)}}
    assert trace != ref

    diffs = trace.diffs_from(ref, strict=False)  # non-strict comparisons
    assert diffs is None


def test_trace_diffs_same_ok_6():  # small score differences
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -20002.1}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -1800.3})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -20002.2}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -1800.4})

    diffs = trace.diffs_from(ref)  # strict comparisons
    assert diffs[0] == {('init', 'score'): {None: (0, 0)},
                        ('stop', 'score'): {None: (1, 1)}}
    assert trace != ref

    diffs = trace.diffs_from(ref, strict=False)  # non-strict comparisons
    assert diffs is None


def test_trace_diffs_same_ok_7():  # small score differences
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.00001}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12346678})

    diffs = trace.diffs_from(ref)  # strict comparisons
    assert diffs[0] == {('add', 'score'): {('B', 'C'): (1, 1)},
                        ('stop', 'score'): {None: (2, 2)}}
    assert trace != ref

    diffs = trace.diffs_from(ref, strict=False)  # non-strict comparisons
    assert diffs is None


def test_trace_diffs_same_ok_8():  # small score differences
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 3.0}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('C', 'D'),
                                       GraphActionDetail.DELTA: 2.0}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0000001}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.5}) \
                   .add(GraphAction.DEL, {GraphActionDetail.ARC: ('C', 'D'),
                                       GraphActionDetail.DELTA: 0.1}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -3.52345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 3.0}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('C', 'D'),
                                     GraphActionDetail.DELTA: 2.0}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.5}) \
                 .add(GraphAction.DEL, {GraphActionDetail.ARC: ('C', 'D'),
                                     GraphActionDetail.DELTA: 0.2}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -3.62345678})

    diffs = trace.diffs_from(ref)  # strict comparisons
    assert diffs[0] == {('add', 'score'): {('B', 'C'): (3, 3)},
                        ('delete', 'score'): {('C', 'D'): (5, 5)},
                        ('stop', 'score'): {None: (6, 6)}}
    print(diffs[2])
    assert trace != ref

    diffs = trace.diffs_from(ref, strict=False)  # non-strict comparisons
    assert diffs is None


def test_trace_diffs_same_ok_9():  # ignore unmatched columns in trace
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0,
                                       GraphActionDetail.ARC_2: ('A', 'B')}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_same_ok_10():  # ignore unmatched columns in ref
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0,
                                     GraphActionDetail.ARC_2: ('A', 'B')}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_same_ok_11():  # accept None values
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.ARC: None}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678,
                                      GraphActionDetail.ARC: None})
    assert trace.diffs_from(ref) is None
    assert trace == ref


def test_trace_diffs_major_ok_1():  # trace has additional entry, same final
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.ARC: None}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678,
                                      GraphActionDetail.ARC: None})
    diffs = trace.diffs_from(ref)
    assert set(diffs[0].keys()) == {('add', 'extra'), ('stop', 'order')}
    assert diffs[0][('add', 'extra')] == {('B', 'C'): (1, None)}
    assert diffs[1] == []
    assert trace != ref
    print('\n{}'.format(diffs[2]))


def test_trace_diffs_major_ok_2():  # trace has additional entry, diff final
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.ARC: None}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                       GraphActionDetail.DELTA: 1.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.ARC: None})
    diffs = trace.diffs_from(ref)
    assert set(diffs[0].keys()) == {('add', 'extra'), ('stop', 'order')}
    assert diffs[0][('add', 'extra')] == {('B', 'C'): (1, None)}
    assert diffs[1] == []
    assert trace != ref
    print('\n{}'.format(diffs[2]))


def test_trace_diffs_major_ok_3():  # trace has missing entry, diff final
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -10.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    diffs = trace.diffs_from(ref)
    assert set(diffs[0].keys()) == {('add', 'missing'), ('stop', 'order')}
    assert diffs[0][('add', 'missing')] == {('B', 'C'): (None, 1)}
    assert diffs[1] == []
    assert trace != ref
    print('\n{}'.format(diffs[2]))


def test_trace_diffs_major_ok_4():  # different arcs added
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('B', 'C'),
                                     GraphActionDetail.DELTA: 1.0}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -9.12345678})
    diffs = trace.diffs_from(ref)
    assert set(diffs[0].keys()) == {('add', 'missing'), ('add', 'extra'),
                                    ('stop', 'score')}
    assert diffs[0][('add', 'missing')] == {('B', 'C'): (None, 1)}
    assert diffs[0][('add', 'extra')] == {('A', 'B'): (1, None)}
    assert diffs[1] == []
    assert trace != ref
    print('\n{}'.format(diffs[2]))

# Compared blocked fields


def test_trace_diffs_blocked_ok_1():  # both blocked are None
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: None}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: None}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    diffs = trace.diffs_from(ref)
    assert diffs is None


def test_trace_diffs_blocked_ok_2():  # both blocked are []
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    diffs = trace.diffs_from(ref)
    assert diffs is None


def test_trace_diffs_blocked_ok_3():  # one None, one [] - no diffs

    # BLOCKED is all None for trace and so BLOCKED is not compared

    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: None}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678})
    diffs = trace.diffs_from(ref)
    assert diffs is None


def test_trace_diffs_blocked_ok_4():  # one None, one [] - diffs

    # BLOCKED has values in each trace so comparison is made which
    # flags minor difference on entry 1.

    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: None}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref)
    assert diffs[0] == {}  # no major differences
    assert diffs[1] == [1]  # minor difference on entry 1


def test_trace_diffs_blocked_ok_5():  # no blocking on any entry

    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})

    diffs = trace.diffs_from(ref)
    assert diffs is None


def test_trace_diffs_blocked_ok_6():  # same block on add

    block = (GraphAction.DEL.value, ('A', 'B'), -2.0, {'elem': 1})

    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0,
                                       GraphActionDetail.BLOCKED: [block]}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0,
                                     GraphActionDetail.BLOCKED: [block]}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref)
    assert diffs is None


def test_trace_diffs_blocked_ok_7():  # difference in block activity

    block = (GraphAction.DEL.value, ('A', 'B'), -2.0, {'elem': 1})
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0,
                                       GraphActionDetail.BLOCKED: [block]}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    block = (GraphAction.REV.value, ('A', 'B'), -2.0, {'elem': 1})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0,
                                     GraphActionDetail.BLOCKED: [block]}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref)
    assert diffs[0] == {}  # no major differences
    assert diffs[1] == [2]  # minor difference on entry 2


def test_trace_diffs_blocked_ok_8():  # difference in block arc

    block = (GraphAction.DEL.value, ('A', 'B'), -2.0, {'elem': 1})
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0,
                                       GraphActionDetail.BLOCKED: [block]}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    block = (GraphAction.DEL.value, ('B', 'A'), -2.0, {'elem': 1})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0,
                                     GraphActionDetail.BLOCKED: [block]}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref)
    assert diffs[0] == {}  # no major differences
    assert diffs[1] == [2]  # minor difference on entry 2


def test_trace_diffs_blocked_ok_9():  # significant difference in block score

    block = (GraphAction.DEL.value, ('A', 'B'), -2.0, {'elem': 1})
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0,
                                       GraphActionDetail.BLOCKED: [block]}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    block = (GraphAction.DEL.value, ('A', 'B'), -1.9, {'elem': 1})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0,
                                     GraphActionDetail.BLOCKED: [block]}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref)
    assert diffs[0] == {}  # no major differences
    assert diffs[1] == [2]  # minor difference on entry 2


def test_trace_diffs_blocked_ok_10():  # insignif. difference in block score

    block = (GraphAction.DEL.value, ('A', 'B'), -2.0, {'elem': 1})
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0,
                                       GraphActionDetail.BLOCKED: [block]}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    block = (GraphAction.DEL.value, ('A', 'B'), -1.9999999, {'elem': 1})
    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0,
                                     GraphActionDetail.BLOCKED: [block]}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref, strict=False)
    assert diffs is None


def test_trace_diffs_blocked_ok_11():  # ordering diff in blocks

    block1 = (GraphAction.DEL.value, ('A', 'B'), -2.0, {'elem': 1})
    block2 = (GraphAction.REV.value, ('A', 'B'), 0.0, {'elem': 1})
    trace = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                        GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 2.0,
                                       GraphActionDetail.BLOCKED: []}) \
                   .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                       GraphActionDetail.DELTA: 0.0,
                                       GraphActionDetail.BLOCKED: [block1, block2]}) \
                   .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                        GraphActionDetail.BLOCKED: []})

    ref = Trace().add(GraphAction.INIT, {GraphActionDetail.DELTA: -10.12345678,
                                      GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.ADD, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 2.0,
                                     GraphActionDetail.BLOCKED: []}) \
                 .add(GraphAction.REV, {GraphActionDetail.ARC: ('A', 'B'),
                                     GraphActionDetail.DELTA: 0.0,
                                     GraphActionDetail.BLOCKED: [block2, block1]}) \
                 .add(GraphAction.STOP, {GraphActionDetail.DELTA: -8.12345678,
                                      GraphActionDetail.BLOCKED: []})
    diffs = trace.diffs_from(ref, strict=False)
    assert diffs is None
