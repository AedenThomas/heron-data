from src.identify_recurring_transactions import identify_recurring_transactions, group_transactions
from src.utils import load_transactions

def main():
    transactions = load_transactions('transactions.json')
    recurring = identify_recurring_transactions(transactions)
    
    grouped_recurring = group_transactions(recurring)
    
    print(f"Found {len(recurring)} recurring transactions in {len(grouped_recurring)} groups:")
    for key, group in grouped_recurring.items():
        print(f"\n{key.capitalize()} ({len(group)} transactions):")
        for transaction in group:
            print(f"  {transaction['date']} - ${transaction['amount']} - {transaction['description']}")

if __name__ == "__main__":
    main()
