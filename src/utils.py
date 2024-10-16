from datetime import datetime
from typing import List, Dict

def load_transactions(file_path: str) -> List[Dict]:
    import json
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['transactions']

def parse_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, '%Y-%m-%d')

def calculate_days_between(date1: datetime, date2: datetime) -> int:
    return abs((date2 - date1).days)
