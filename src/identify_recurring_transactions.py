from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from .utils import parse_date, calculate_days_between
import re

def find_common_substring(strings):
    if not strings:
        return ""
    shortest = min(strings, key=len)
    for i in range(len(shortest), 0, -1):
        substring = shortest[:i]
        if all(substring in s for s in strings):
            return substring
    return ""

def group_transactions(transactions: List[Dict]) -> Dict[str, List[Dict]]:
    groups = defaultdict(list)
    for transaction in transactions:
        desc = transaction['description'].lower()
        # Remove date-like patterns from the beginning of the description
        desc = re.sub(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\d{4}\s*', '', desc)
        key = find_common_substring([desc] + [g[0]['description'].lower() for g in groups.values() if g])
        if key and len(key) > 3:
            groups[key].append(transaction)
        else:
            groups[desc].append(transaction)
    
    return {k: v for k, v in groups.items() if len(v) >= 2}

def identify_recurring_transactions(transactions: List[Dict]) -> List[Dict]:
    grouped_transactions = group_transactions(transactions)
    
    recurring_transactions = []
    
    for key, group in grouped_transactions.items():
        # print(f"Analyzing group: {key} with {len(group)} transactions")  # Debug print
        
        sorted_group = sorted(group, key=lambda x: parse_date(x['date']))
        intervals = [
            calculate_days_between(parse_date(sorted_group[i]['date']), parse_date(sorted_group[i+1]['date']))
            for i in range(len(sorted_group) - 1)
        ]
        
        # print(f"Intervals for {key}: {intervals}")  # Debug print
        
        if len(group) >= 2:  # Changed from 3 to 2
            avg_interval = sum(intervals) / len(intervals)
            if 25 <= avg_interval <= 35:  # Monthly (allowing more variation)
                recurring_transactions.extend(sorted_group)
                # print(f"Added {key} as recurring (monthly, avg interval: {avg_interval})")
            elif 6 <= avg_interval <= 8:  # Weekly
                recurring_transactions.extend(sorted_group)
                # print(f"Added {key} as recurring (weekly, avg interval: {avg_interval})")
            else:
                # Check if at least 75% of intervals are within 28-35 days (monthly with more flexibility)
                monthly_count = sum(1 for interval in intervals if 28 <= interval <= 35)
                if monthly_count >= len(intervals) * 0.75:
                    recurring_transactions.extend(sorted_group)
                    # print(f"Added {key} as recurring (flexible monthly pattern)")
    
    return recurring_transactions
