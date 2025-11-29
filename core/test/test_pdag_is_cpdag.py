
# Test PDAG.is_cpdag() method

import pytest

from causaliq_core.graph import is_cpdag
import testdata.example_dags as dag
import testdata.example_pdags as pdag


def test_pdag_is_cpdag_empty_ok():  # empty graph
    assert is_cpdag(pdag.empty()) is True


def test_pdag_is_cpdag_a_ok():  # single node DAG
    assert is_cpdag(pdag.a()) is True


def test_pdag_is_cpdag_ab_ok():  # A -> B chain
    assert is_cpdag(pdag.ab()) is False


def test_pdag_is_cpdag_ab_2_ok():  # A -> B chain
    assert is_cpdag(pdag.ab_2()) is False


def test_pdag_is_cpdag_ba_ok():  # B -> A chain
    assert is_cpdag(pdag.ba()) is False


def test_pdag_is_cpdag_a_b_ok():  # A, B unconnected
    assert is_cpdag(pdag.a_b()) is True


def test_pdag_is_cpdag_ab3_ok():  # A - B PDAG
    assert is_cpdag(pdag.ab3()) is True


def test_pdag_is_cpdag_a_b_c_ok():  # A, B, C unconnected
    assert is_cpdag(pdag.a_b_c()) is True


def test_pdag_is_cpdag_ac_b_ok():  # A -> C, B
    assert is_cpdag(pdag.ac_b()) is False


def test_pdag_is_cpdag_ac_b2_ok():  # A - C, B
    assert is_cpdag(pdag.ac_b2()) is True


def test_pdag_is_cpdag_abc_ok():  # A -> B -> C
    assert is_cpdag(pdag.abc()) is False


def test_pdag_is_cpdag_abc2_ok():  # A -> B -> C
    assert is_cpdag(pdag.abc2()) is False


def test_pdag_is_cpdag_abc3_ok():  # A - B -> C
    assert is_cpdag(pdag.abc3()) is False


def test_pdag_is_cpdag_abc4_ok():  # A - B - C
    assert is_cpdag(pdag.abc4()) is True


def test_pdag_is_cpdag_abc5_ok():  # A -> B - C
    assert is_cpdag(pdag.abc5()) is False


def test_pdag_is_cpdag_abc6_ok():  # C - A - B
    assert is_cpdag(pdag.abc6()) is True


def test_pdag_is_cpdag_ab_ac_ok():  # B <- A -> C - common cause
    assert is_cpdag(pdag.ab_ac()) is False


def test_pdag_is_cpdag_ba_bc_ok():  # A <- B -> C - common cause
    assert is_cpdag(pdag.ba_bc()) is False


def test_pdag_is_cpdag_ac_bc_ok():  # A -> C <- B - common effect
    assert is_cpdag(pdag.ac_bc()) is True


def test_pdag_is_cpdag_ab_cb_ok():  # A -> B <- C - common effect
    assert is_cpdag(pdag.ab_cb()) is True


def test_pdag_is_cpdag_abc_acyclic_ok():  # A -> B -> C <- A
    assert is_cpdag(pdag.abc_acyclic()) is False


def test_pdag_is_cpdag_abc_acyclic2_ok():  # A -> B -> C - A
    assert is_cpdag(pdag.abc_acyclic2()) is False


def test_pdag_is_cpdag_abc_acyclic3_ok():  # A -- B -- C, A --> C
    assert is_cpdag(pdag.abc_acyclic3()) is False


def test_pdag_is_cpdag_abc_acyclic4_ok():  # A -- B -- C -- A
    assert is_cpdag(pdag.abc_acyclic4()) is True


def test_pdag_is_cpdag_cancer1_OK():  # 5-node CANCER DAG as a PDAG
    assert is_cpdag(pdag.cancer1()) is True


def test_pdag_is_cpdag_cancer2_OK():  # 5-node CANCER PDAG with 2 undir. edges
    assert is_cpdag(pdag.cancer2()) is False


def test_pdag_is_cpdag_cancer3_OK():  # 5-node CANCER skeleton PDAG
    assert is_cpdag(pdag.cancer3()) is True


def test_pdag_is_cpdag_asia1_OK():  # Asia PDAG
    assert is_cpdag(pdag.asia()) is True


def test_pdag_is_cpdag_asia2_OK():  # Asia DAG
    assert is_cpdag(dag.asia()) is False


# Exemplar 4 node PDAGs from Andersson et al., 1995

def test_pdag_is_cpdag_and4_1a_OK():  # 1  2  3  4 DAG
    assert is_cpdag(dag.and4_1()) is True


def test_pdag_is_cpdag_and4_1b_OK():  # 1  2  3  4 PDAG
    assert is_cpdag(pdag.and4_1()) is True


def test_pdag_is_cpdag_and4_2a_OK():  # 1 -> 2  3  4 DAG
    assert is_cpdag(dag.and4_2()) is False


def test_pdag_is_cpdag_and4_2b_OK():  # 1 - 2  3  4 PDAG
    assert is_cpdag(pdag.and4_2()) is True


def test_pdag_is_cpdag_and4_3a_OK():  # 1 -> 2  3 -> 4 DAG
    assert is_cpdag(dag.and4_3()) is False


def test_pdag_is_cpdag_and4_3b_OK():  # 1 - 2  3 - 4 PDAG
    assert is_cpdag(pdag.and4_3()) is True


def test_pdag_is_cpdag_and4_4a_OK():  # 1 <- 2 <- 3  4 PDAG
    assert is_cpdag(dag.and4_4()) is False


def test_pdag_is_cpdag_and4_4b_OK():  # 1 - 2 - 3  4 PDAG
    assert is_cpdag(pdag.and4_4()) is True


def test_pdag_is_cpdag_and4_5a_OK():  # 1 -> 2 <- 3  4 DAG
    assert is_cpdag(dag.and4_5()) is True


def test_pdag_is_cpdag_and4_5b_OK():  # 1 -> 2 <- 3  4 PDAG
    assert is_cpdag(pdag.and4_5()) is True


def test_pdag_is_cpdag_and4_6a_OK():  # 1 <- 2 <- 3 -> 1  4 DAG
    assert is_cpdag(dag.and4_6()) is False


def test_pdag_is_cpdag_and4_6b_OK():  # 1 - 2 - 3 - 1  4 PDAG
    assert is_cpdag(pdag.and4_6()) is True


def test_pdag_is_cpdag_and4_7a_OK():  # 1 <- 2 <- 3 <- 4 DAG
    assert is_cpdag(dag.and4_7()) is False


def test_pdag_is_cpdag_and4_7b_OK():  # 1 - 2 - 3 - 4 PDAG
    assert is_cpdag(pdag.and4_7()) is True


def test_pdag_is_cpdag_and4_8a_OK():  # 1 -> 2 <- 3 <- 4 DAG
    assert is_cpdag(dag.and4_8()) is False


def test_pdag_is_cpdag_and4_8b_OK():  # 1 -> 2 <- 3 - 4 PDAG
    assert is_cpdag(pdag.and4_8()) is True


def test_pdag_is_cpdag_and4_9a_OK():  # 3 <- 2 -> 1, 2 <- 4 DAG
    assert is_cpdag(dag.and4_9()) is False


def test_pdag_is_cpdag_and4_9b_OK():  # 3 - 2 - 1, 2 - 4 (undir. star) PDAG
    assert is_cpdag(pdag.and4_9()) is True


def test_pdag_is_cpdag_and4_10a_OK():  # 1 -> 2 -> 4, 3 -> 2 DAG
    assert is_cpdag(dag.and4_10()) is True


def test_pdag_is_cpdag_and4_10b_OK():  # 1 -> 2 -> 4, 3 -> 2 PDAG
    assert is_cpdag(pdag.and4_10()) is True


def test_pdag_is_cpdag_and4_11a_OK():  # 1 -> 2 <- 4, 3 -> 2 (star coll) DAG
    assert is_cpdag(dag.and4_11()) is True


def test_pdag_is_cpdag_and4_11b_OK():  # 1 -> 2 <- 4, 3 -> 2 (star coll) PDAG
    assert is_cpdag(pdag.and4_11()) is True


def test_pdag_is_cpdag_and4_12a_OK():  # 2 -> 3 -> 1 <- 2 <- 4 DAG
    assert is_cpdag(dag.and4_12()) is False


def test_pdag_is_cpdag_and4_12b_OK():  # 2 - 3 - 1 - 2 - 4 PDAG
    assert is_cpdag(pdag.and4_12()) is True


def test_pdag_is_cpdag_and4_13a_OK():  # 2 <- 1 <- 3 -> 2 <- 4 DAG
    assert is_cpdag(dag.and4_13()) is False


def test_pdag_is_cpdag_and4_13b_OK():  # 2 <- 1 - 3 -> 2 <- 4 PDAG
    assert is_cpdag(pdag.and4_13()) is True


def test_pdag_is_cpdag_and4_14a_OK():  # 2 <- 1 -> 3 <- 2 <- 4 DAG
    assert is_cpdag(dag.and4_14()) is True


def test_pdag_is_cpdag_and4_14b_OK():  # 2 <- 1 -> 3 <- 2 <- 4 PDAG
    assert is_cpdag(pdag.and4_14()) is True


def test_pdag_is_cpdag_and4_15a_OK():  # 2->4<-3, 2<-1->3 (square, 1 coll) DAG
    assert is_cpdag(dag.and4_15()) is False


def test_pdag_is_cpdag_and4_15b_OK():  # 2->4<-3, 2-1-3 (square, 1 coll) PDAG
    assert is_cpdag(pdag.and4_15()) is True


def test_pdag_is_cpdag_and4_16a_OK():  # 2->4<-3, 2->1<-3 (square colls) DAG
    assert is_cpdag(dag.and4_16()) is True


def test_pdag_is_cpdag_and4_16b_OK():  # 2->4<-3, 2->1<-3 (square colls) PDAG
    assert is_cpdag(pdag.and4_16()) is True


def test_pdag_is_cpdag_and4_17a_OK():  # 1<-4->2<-1<-3<-1 (0 col sq + diag) DAG
    assert is_cpdag(dag.and4_17()) is False


def test_pdag_is_cpdag_and4_17b_OK():  # 1-4-2-1-3<-1 (sq + diag undir) PDAG
    assert is_cpdag(pdag.and4_17()) is True


def test_pdag_is_cpdag_complete4a_OK():  # complete DAG
    assert is_cpdag(dag.complete4()) is False


def test_pdag_is_cpdag_complete4b_OK():  # complete undir PDAG
    assert is_cpdag(pdag.complete4()) is True


def test_pdag_is_cpdag_value_error_1():  # 1-2-3-4-1 (unextendable square)
    with pytest.raises(ValueError):
        is_cpdag(pdag.and4_inv1())
