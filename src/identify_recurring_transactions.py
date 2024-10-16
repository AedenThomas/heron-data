from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from .utils import parse_date, calculate_days_between

def identify_recurring_transactions(transactions: List[Dict]) -> List[Dict]:
    # Group transactions by description
    grouped_transactions = defaultdict(list)
    for transaction in transactions:
        grouped_transactions[transaction['description']].append(transaction)
    
    recurring_transactions = []
    
    for description, group in grouped_transactions.items():
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
        if len(set(intervals)) == 1 and intervals[0] <= 31:  # Assuming monthly or more frequent
            recurring_transactions.extend(sorted_group)
        elif len(set(intervals)) <= 2 and max(intervals) <= 32:  # Allow some flexibility
            recurring_transactions.extend(sorted_group)
    
    return recurring_transactions
