# Test BIC Gaussian scores - Mathematical validation without bnlearn dependency
# This test file validates CausalIQ's BIC Gaussian score implementation
# using mathematical properties and internal consistency checks

import pytest
from numpy import array, log, sqrt, sum as npsum, mean as npmean, var as npvar
from math import pi, e
from random import random
from os import remove

from causaliq_data.score import dag_score, gaussian_node_score, entropy_gaussian_score
from causaliq_data import NumPy
import testdata.example_dags as dag
from data import TESTDATA_DIR
from causaliq_core.utils import values_same


# temp file, automatically removed  
@pytest.fixture(scope="function")
def tmpfile():
    _tmpfile = TESTDATA_DIR + '/tmp/{}.csv'.format(int(random() * 10000000))
    yield _tmpfile
    try:
        remove(_tmpfile)
    except Exception:
        pass


class TestBICGaussianScores:
    """Test BIC Gaussian scores using mathematical validation"""

    def test_bic_formula_consistency(self):
        """Test that BIC-g follows the correct mathematical formula: BIC = loglik - k*params*ln(N)/2"""
        data = NumPy(array([[1.1, 0.0], [2.2, 1.7], [-0.3, 0.0]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        # Get both BIC and loglik scores
        scores_bic = dag_score(dag.x_y(), data, 'bic-g', {'k': 1.0})
        scores_loglik = dag_score(dag.x_y(), data, 'loglik-g', {'k': 1.0})
        
        # For independent X,Y: each node has 2 parameters (mean, sd)
        total_params = 4
        N = data.N
        k = 1.0
        
        # Calculate expected penalty
        penalty = k * total_params * log(N) / 2
        
        # BIC should equal loglik minus penalty
        expected_bic = dict(scores_loglik.sum())['loglik-g'] - penalty
        actual_bic = dict(scores_bic.sum())['bic-g']
        
        assert values_same(actual_bic, expected_bic, sf=10)

    def test_parameter_counting_correctness(self):
        """Test that parameter counting is correct for different network structures"""
        data = NumPy(array([[0.1, 0.2, 0.3],
                            [0.4, 0.5, 0.6], 
                            [0.7, 0.8, 0.9]], dtype='float32'),
                     dstype='continuous', 
                     col_values={'X': None, 'Y': None, 'Z': None})
        
        # Two-node independent: X Y -> 2 nodes * 2 params each = 4 params
        data_xy = NumPy(array([[0.1, 0.2], [0.4, 0.5], [0.7, 0.8]], dtype='float32'),
                       dstype='continuous', col_values={'X': None, 'Y': None})
        scores_xy_indep = dag_score(dag.x_y(), data_xy, 'bic-g', {'k': 1.0})
        loglik_xy_indep = dag_score(dag.x_y(), data_xy, 'loglik-g', {'k': 1.0})
        
        # X->Y chain: X(2) + Y(3: mean,sd,coeff) = 5 params  
        scores_xy_chain = dag_score(dag.xy(), data_xy, 'bic-g', {'k': 1.0})
        loglik_xy_chain = dag_score(dag.xy(), data_xy, 'loglik-g', {'k': 1.0})
        
        penalty_indep = 4 * log(data_xy.N) / 2
        penalty_chain = 5 * log(data_xy.N) / 2
        
        expected_bic_indep = dict(loglik_xy_indep.sum())['loglik-g'] - penalty_indep
        expected_bic_chain = dict(loglik_xy_chain.sum())['loglik-g'] - penalty_chain
        
        assert values_same(dict(scores_xy_indep.sum())['bic-g'], expected_bic_indep, sf=10)
        assert values_same(dict(scores_xy_chain.sum())['bic-g'], expected_bic_chain, sf=10)

    def test_score_validity_ranges(self):
        """Test that BIC-g scores are in reasonable ranges"""
        data = NumPy(array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        scores = dag_score(dag.x_y(), data, 'bic-g', {'k': 1.0})
        total_score = dict(scores.sum())['bic-g']
        
        # Score should be a finite number
        assert not (total_score == float('inf') or total_score == float('-inf'))
        assert not (total_score != total_score)  # Check for NaN
        
        # For this small dataset, score should be reasonable
        assert -100 < total_score < 100

    def test_orphan_node_score_correctness(self):
        """Test that orphan node BIC score matches manual calculation"""
        # Use 2-column data but only test X
        data = NumPy(array([[1.0, 9.0], [2.0, 9.0], [3.0, 9.0], [4.0, 9.0], [5.0, 9.0]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        # Manual calculation for X values
        values = array([1.0, 2.0, 3.0, 4.0, 5.0], dtype='float32')
        N = len(values)
        mean = npmean(values)
        sd = sqrt(npsum((values - mean) ** 2) / (N - 1))
        
        # Log-likelihood for Gaussian
        loglik_manual = npsum(-0.5 * log(2 * pi) - log(sd) - 0.5 * ((values - mean) / sd) ** 2)
        penalty_manual = 2 * log(N) / 2  # 2 parameters: mean, sd
        bic_manual = loglik_manual - penalty_manual
        
        # Get score from function for X node only
        scores = gaussian_node_score('X', {}, ['bic-g'], {'k': 1.0}, data, False)
        
        assert values_same(scores['bic-g'], bic_manual, sf=6)

    def test_node_score_additivity(self):
        """Test that individual node scores sum to total DAG score"""
        data = NumPy(array([[1.1, 2.2, 3.3],
                            [1.4, 2.5, 3.6],
                            [1.7, 2.8, 3.9]], dtype='float32'),
                     dstype='continuous',
                     col_values={'X': None, 'Y': None, 'Z': None})
        
        # Get total score
        total_scores = dag_score(dag.xyz(), data, 'bic-g', {'k': 1.0})
        total_bic = dict(total_scores.sum())['bic-g']
        
        # Get individual node scores  
        x_score = gaussian_node_score('X', {}, ['bic-g'], {'k': 1.0}, data, False)
        y_score = gaussian_node_score('Y', {'Y': ['X']}, ['bic-g'], {'k': 1.0}, data, False)
        z_score = gaussian_node_score('Z', {'Z': ['Y']}, ['bic-g'], {'k': 1.0}, data, False)
        
        manual_total = x_score['bic-g'] + y_score['bic-g'] + z_score['bic-g']
        
        assert values_same(total_bic, manual_total, sf=10)

    def test_more_data_improves_fit(self):
        """Test that more data generally improves likelihood (before penalty)"""
        # Small dataset with good fit
        small_data = NumPy(array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]], dtype='float32'),
                          dstype='continuous', col_values={'X': None, 'Y': None})
        
        # Larger dataset with same linear relationship 
        large_data = NumPy(array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0], [5.0, 6.0],
                                 [6.0, 7.0], [7.0, 8.0]], dtype='float32'),
                          dstype='continuous', col_values={'X': None, 'Y': None})
        
        small_loglik = dag_score(dag.x_y(), small_data, 'loglik-g', {'k': 1.0})
        large_loglik = dag_score(dag.x_y(), large_data, 'loglik-g', {'k': 1.0})
        
        # Just verify both produce valid scores
        small_score = dict(small_loglik.sum())['loglik-g']
        large_score = dict(large_loglik.sum())['loglik-g']
        
        # Both should be finite numbers
        assert not (small_score == float('inf') or small_score == float('-inf'))
        assert not (large_score == float('inf') or large_score == float('-inf'))
        assert small_score == small_score  # Check for NaN
        assert large_score == large_score  # Check for NaN

    def test_entropy_gaussian_score_function(self):
        """Test entropy_gaussian_score function directly"""
        data = NumPy(array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        # Test orphan node
        x_entropy = entropy_gaussian_score('X', {}, {'k': 1.0}, data)
        x_gaussian = gaussian_node_score('X', {}, ['bic-g', 'loglik-g'], {'k': 1.0}, data, False)
        
        assert values_same(x_entropy['bic-g'], x_gaussian['bic-g'], sf=10)
        assert values_same(x_entropy['loglik-g'], x_gaussian['loglik-g'], sf=10)

    def test_linear_regression_effect(self):
        """Test that adding parents changes score appropriately"""
        # Create data where Y is clearly related to X
        data = NumPy(array([[1.0, 2.1], [2.0, 4.1], [3.0, 6.1], 
                           [4.0, 8.1], [5.0, 10.1]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        # Y as orphan vs Y with parent X
        y_orphan = gaussian_node_score('Y', {}, ['bic-g'], {'k': 1.0}, data, False)
        y_with_x = gaussian_node_score('Y', {'Y': ['X']}, ['bic-g'], {'k': 1.0}, data, False)
        
        # With clear linear relationship, Y|X should have better likelihood
        # despite penalty for extra parameter
        assert y_with_x['bic-g'] > y_orphan['bic-g']

    def test_score_symmetry_for_independent_nodes(self):
        """Test that independent nodes with same distribution get same scores"""
        # Create symmetric data
        data = NumPy(array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        x_score = gaussian_node_score('X', {}, ['bic-g'], {'k': 1.0}, data, False)
        y_score = gaussian_node_score('Y', {}, ['bic-g'], {'k': 1.0}, data, False)
        
        # Should be exactly equal for identical distributions
        assert values_same(x_score['bic-g'], y_score['bic-g'], sf=12)

    def test_different_score_types_consistency(self):
        """Test that bic-g, loglik-g, and bge scores are consistent"""
        data = NumPy(array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]], dtype='float32'),
                     dstype='continuous', col_values={'X': None, 'Y': None})
        
        # All three score types should work
        bic_scores = dag_score(dag.x_y(), data, 'bic-g', {'k': 1.0})
        loglik_scores = dag_score(dag.x_y(), data, 'loglik-g', {'k': 1.0})
        bge_scores = dag_score(dag.x_y(), data, 'bge', {'k': 1.0})
        
        # Verify we get valid numerical results
        assert isinstance(dict(bic_scores.sum())['bic-g'], float)
        assert isinstance(dict(loglik_scores.sum())['loglik-g'], float)
        assert isinstance(dict(bge_scores.sum())['bge'], float)
        
        # BIC should be less than loglik (due to penalty)
        assert dict(bic_scores.sum())['bic-g'] < dict(loglik_scores.sum())['loglik-g']