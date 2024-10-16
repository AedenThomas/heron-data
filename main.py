from src.identify_recurring_transactions import identify_recurring_transactions
from src.utils import load_transactions

def main():
    transactions = load_transactions('transactions.json')
    recurring = identify_recurring_transactions(transactions)
    
    print(f"Found {len(recurring)} recurring transactions:")
    for transaction in recurring:
        print(f"{transaction['description']} - {transaction['date']} - ${transaction['amount']}")

if __name__ == "__main__":
    main()
