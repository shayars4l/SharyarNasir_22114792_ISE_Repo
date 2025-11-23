# tests/test_blackbox.py
import unittest
import os
from loader import load_services
from calculator import calculate_all_costs, calculate_service_cost

class BlackBoxTests(unittest.TestCase):
    def setUp(self):
        # load sample services.csv from repo root
        self.services = load_services(os.path.join(os.path.dirname(__file__), '..', 'services.csv'))

    def test_load_services_contains_compute(self):
        self.assertIn("Compute", self.services)
        self.assertEqual(self.services["Compute"]["units"], "hour")

    def test_simple_compute_cost(self):
        # 100 hours should use 0.58 per sample
        subs = {"Compute": 100}
        breakdown = calculate_all_costs(self.services, subs)
        self.assertIn("Compute", breakdown)
        self.assertAlmostEqual(breakdown["Compute"]["per_unit"], 0.58, places=2)
        self.assertAlmostEqual(breakdown["Compute"]["cost"], 100 * 0.58, places=2)

    def test_multiple_services_total(self):
        subs = {"Compute": 100, "Storage": 200}
        breakdown = calculate_all_costs(self.services, subs)
        expected_total = round(100 * 0.58 + 200 * 0.10, 2)
        self.assertAlmostEqual(breakdown["TOTAL"], expected_total, places=2)

if __name__ == '__main__':
    unittest.main()
