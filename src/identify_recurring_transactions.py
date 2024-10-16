from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from .utils import parse_date, calculate_days_between
import re

def group_transactions(transactions: List[Dict]) -> Dict[str, List[Dict]]:
    groups = defaultdict(list)
    for transaction in transactions:
        desc = transaction['description'].lower()
        desc = re.sub(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\d{4}\s*', '', desc)
        desc = re.sub(r':.*$', '', desc)
        desc = desc.strip()
        if len(desc) > 3:
            groups[desc].append(transaction)
    
    return {k: v for k, v in groups.items() if len(v) >= 2}

def identify_recurring_transactions(transactions: List[Dict]) -> List[Dict]:
    grouped_transactions = group_transactions(transactions)
    
    recurring_transactions = []
    
    for key, group in grouped_transactions.items():
        sorted_group = sorted(group, key=lambda x: parse_date(x['date']))
        intervals = [
            calculate_days_between(parse_date(sorted_group[i]['date']), parse_date(sorted_group[i+1]['date']))
            for i in range(len(sorted_group) - 1)
        ]
        
        if len(group) >= 2:
            avg_interval = sum(intervals) / len(intervals) if intervals else 0
            if 25 <= avg_interval <= 35:  # Monthly
                recurring_transactions.extend(sorted_group)
            elif 6 <= avg_interval <= 8:  # Weekly
                recurring_transactions.extend(sorted_group)
            else:
                # Check if at least 75% of intervals are within 28-35 days (flexible monthly)
                monthly_count = sum(1 for interval in intervals if 28 <= interval <= 35)
                if monthly_count >= len(intervals) * 0.75:
                    recurring_transactions.extend(sorted_group)
    

    return recurring_transactions

