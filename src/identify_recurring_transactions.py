from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from .utils import parse_date, calculate_days_between

def identify_recurring_transactions(transactions: List[Dict]) -> List[Dict]:
    grouped_transactions = defaultdict(list)
    for transaction in transactions:
        key = transaction['description'].lower().split(':')[0]
        grouped_transactions[key].append(transaction)
    
    recurring_transactions = []
    
    for key, group in grouped_transactions.items():
        print(f"Analyzing group: {key} with {len(group)} transactions")  # Debug print
        if len(group) < 2:
            continue
        
        sorted_group = sorted(group, key=lambda x: parse_date(x['date']))
        intervals = [
            calculate_days_between(parse_date(sorted_group[i]['date']), parse_date(sorted_group[i+1]['date']))
            for i in range(len(sorted_group) - 1)
        ]
        
        print(f"Intervals for {key}: {intervals}")  # Debug print
        
        if len(set(intervals)) <= 2:  # Allow some flexibility
            avg_interval = sum(intervals) / len(intervals)
            if 25 <= avg_interval <= 35 or 6 <= avg_interval <= 8:  # Monthly or Weekly
                recurring_transactions.extend(sorted_group)
                print(f"Added {key} as recurring (avg interval: {avg_interval})")  # Debug print
        elif len(group) >= 3:  # Check for monthly patterns with more flexibility
            monthly_count = sum(1 for interval in intervals if 28 <= interval <= 31)
            if monthly_count >= len(intervals) * 0.75:  # At least 75% of intervals are monthly
                recurring_transactions.extend(sorted_group)
                print(f"Added {key} as recurring (monthly pattern)")  # Debug print
    
    return recurring_transactions
