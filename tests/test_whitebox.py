# tests/test_whitebox.py
import unittest
from calculator import calculate_service_cost
from loader import load_services
import os

class WhiteBoxTests(unittest.TestCase):
    def setUp(self):
        self.services = load_services(os.path.join(os.path.dirname(__file__), '..', 'services.csv'))

    def test_tier_boundary_exact_start(self):
        # If amount == tier start value, choose that tier
        compute_def = self.services["Compute"]
        # tier starts: 0,50,1000,8000 -> test amount exactly 50
        cost = calculate_service_cost(compute_def, 50)
        # at 50 should use per_unit 0.58
        self.assertAlmostEqual(cost, 50 * 0.58, places=5)

    def test_zero_amount(self):
        compute_def = self.services["Compute"]
        cost = calculate_service_cost(compute_def, 0)
        self.assertEqual(cost, 0)

    def test_high_amount_last_tier(self):
        compute_def = self.services["Compute"]
        # high amount to ensure last tier selected
        cost = calculate_service_cost(compute_def, 100000)
        self.assertAlmostEqual(cost, 100000 * 0.52, places=2)

    def test_negative_amount_raises(self):
        compute_def = self.services["Compute"]
        with self.assertRaises(ValueError):
            calculate_service_cost(compute_def, -5)

if __name__ == '__main__':
    unittest.main()
