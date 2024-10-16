# tests/test_identify_recurring_transactions.py

import unittest
from datetime import datetime, timedelta
from src.identify_recurring_transactions import identify_recurring_transactions, group_transactions

class TestIdentifyRecurringTransactions(unittest.TestCase):

    def generate_transactions(self, description, amount, start_date, count, interval_days):
        return [
            {
                "description": f"{description}",
                "amount": amount,
                "date": (start_date + timedelta(days=i*interval_days)).strftime("%Y-%m-%d")
            }
            for i in range(count)
        ]

    def test_identify_spotify_subscription(self):
        transactions = self.generate_transactions("Spotify", -14.99, datetime(2021, 1, 1), 4, 30)
        result = identify_recurring_transactions(transactions)
        self.assertEqual(len(result), 4)
        self.assertTrue(all("spotify" in t["description"].lower() for t in result))

    def test_identify_salary_payments(self):
        transactions = self.generate_transactions("Acme Corp Salary", 5000, datetime(2021, 1, 1), 6, 30)
        result = identify_recurring_transactions(transactions)
        self.assertEqual(len(result), 6)
        self.assertTrue(all("acme corp salary" in t["description"].lower() for t in result))

    def test_identify_weekly_payments(self):
        transactions = self.generate_transactions("Weekly Payment", 100, datetime(2021, 1, 1), 8, 7)
        result = identify_recurring_transactions(transactions)
        self.assertEqual(len(result), 8)
        self.assertTrue(all("weekly payment" in t["description"].lower() for t in result))

    def test_non_recurring_transactions(self):
        transactions = [
            {"description": "One-off purchase", "amount": -50, "date": "2021-01-01"},
            {"description": "Another one-off", "amount": -75, "date": "2021-02-15"},
            {"description": "Random expense", "amount": -30, "date": "2021-03-22"}
        ]
        result = identify_recurring_transactions(transactions)
        self.assertEqual(len(result), 0)

    def test_mixed_transactions(self):
        recurring = self.generate_transactions("Recurring", 100, datetime(2021, 1, 1), 4, 30)
        non_recurring = [
            {"description": "One-off", "amount": -50, "date": "2021-01-15"},
            {"description": "Another one-off", "amount": -75, "date": "2021-02-20"}
        ]
        transactions = recurring + non_recurring
        result = identify_recurring_transactions(transactions)
        self.assertEqual(len(result), 4)
        self.assertTrue(all("recurring" in t["description"].lower() for t in result))

    def test_group_transactions(self):
        transactions = [
            {"description": "Spotify", "amount": -14.99, "date": "2021-01-01"},
            {"description": "Spotify", "amount": -14.99, "date": "2021-02-01"},
            {"description": "Netflix", "amount": -19.99, "date": "2021-01-15"},
            {"description": "Netflix", "amount": -19.99, "date": "2021-02-15"},
            {"description": "Company Lunch: Burritos", "amount": -5.00, "date": "2021-03-01"},
            {"description": "Company Lunch: Korean", "amount": -5.00, "date": "2021-03-08"},
            {"description": "One-off purchase", "amount": -50, "date": "2021-01-10"}
        ]
        groups = group_transactions(transactions)
        self.assertEqual(len(groups), 3)  # Spotify, Netflix, Company Lunch
        self.assertIn("spotify", groups)
        self.assertIn("netflix", groups)
        self.assertIn("company lunch", groups)
        self.assertEqual(len(groups["spotify"]), 2)
        self.assertEqual(len(groups["netflix"]), 2)
        self.assertEqual(len(groups["company lunch"]), 2)


if __name__ == '__main__':
    unittest.main()
