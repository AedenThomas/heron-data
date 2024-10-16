from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from .utils import parse_date, calculate_days_between

def identify_recurring_transactions(transactions: List[Dict]) -> List[Dict]:
    # Group transactions by similar descriptions
    grouped_transactions = defaultdict(list)
    for transaction in transactions:
        key = transaction['description'].lower().split(':')[0]  # Group by first part of description
        grouped_transactions[key].append(transaction)
    
    recurring_transactions = []
    
    for group in grouped_transactions.values():
        if len(group) < 2:
            continue
        
        # Sort transactions by date
        sorted_group = sorted(group, key=lambda x: parse_date(x['date']))
        
        # Calculate intervals between transactions
        intervals = [
            calculate_days_between(parse_date(sorted_group[i]['date']), parse_date(sorted_group[i+1]['date']))
            for i in range(len(sorted_group) - 1)
        ]
        
        # Check if intervals are consistent
        if len(set(intervals)) <= 2:  # Allow some flexibility
            avg_interval = sum(intervals) / len(intervals)
            if 25 <= avg_interval <= 35:  # Monthly
                recurring_transactions.extend(sorted_group)
            elif 6 <= avg_interval <= 8:  # Weekly
                recurring_transactions.extend(sorted_group)
    
    return recurring_transactions
