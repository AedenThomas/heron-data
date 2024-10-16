from src.identify_recurring_transactions import identify_recurring_transactions
from src.utils import load_transactions
from collections import defaultdict

def main():
    transactions = load_transactions('transactions.json')
    recurring = identify_recurring_transactions(transactions)
    
    # Group recurring transactions by description
    grouped_recurring = defaultdict(list)
    for transaction in recurring:
        key = transaction['description'].lower().split(':')[0]
        grouped_recurring[key].append(transaction)
    
    print(f"Found {len(recurring)} recurring transactions in {len(grouped_recurring)} groups:")
    for key, group in grouped_recurring.items():
        print(f"\n{key.capitalize()} ({len(group)} transactions):")
        for transaction in group:
            print(f"  {transaction['date']} - ${transaction['amount']} - {transaction['description']}")

if __name__ == "__main__":
    main()
