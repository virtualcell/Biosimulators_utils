from biosimulators_utils.simulator import utils
from biosimulators_utils.simulator.data_model import AlgorithmSubstitutionPolicy
from unittest import mock
import os
import unittest


class SimulatorUtilsTestCase(unittest.TestCase):
    def test_get_algorithm_substitution_policy(self):
        self.assertEqual(utils.get_algorithm_substitution_policy(), AlgorithmSubstitutionPolicy.SAME_FRAMEWORK)

        with mock.patch.dict(os.environ, {'ALGORITHM_SUBSTITUTION_POLICY': 'ANY'}):
            self.assertEqual(utils.get_algorithm_substitution_policy(), AlgorithmSubstitutionPolicy.ANY)

        with mock.patch.dict(os.environ, {'ALGORITHM_SUBSTITUTION_POLICY': 'UNDEFINED'}):
            with self.assertRaises(ValueError):
                utils.get_algorithm_substitution_policy()
