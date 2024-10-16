# Heron Data Challenge

This project identifies recurring transactions from a set of bank transactions.

## Approach

1. Group transactions by similar descriptions
2. For each group with at least 2 transactions:
   a. sort transactions by date
   b. calculate intervals between consecutive transactions
   c. check if intervals are consistent (monthly or weekly patterns)
   d. if intervals are consistent, consider the transactions as recurring

## Development Process and Problem Solving

### 1. Initial Implementation
Basic implementation that grouped transactions by exact description matches and looked for consistent intervals between transactions. PRoblems:
- It only identified monthly recurring transactions
- It required exact description matches, missing transactions with slight variations
- It didn't handle weekly recurring transactions

WOrked for spotify subscriptions but missed many other types of recurring transactions.

### 2. Handling Varying Descriptions
Transactions like salary payments had varying descriptions (e.g., "Jan2021 Acme Corp Salary", "Feb2021 Acme Corp Salary"). so i implemented a regex based approach to remove date like patterns from the beginning of descriptions.

### 3. Grouping Similar Transactions
Initial grouping was too strict, missing transactions that were similar but not identical. so i removed the `find_common_substring` function entirely and implemented a simpler, more efficient regex-based approach.

### 4. Identifying Weekly Transactions
Initial implementation missed weekly recurring transactions like company lunches. so i added specific criteria for weekly transactions, considering intervals between 6 and 8 days.

### 5. Handling Edge Cases

The algorithm sometimes failed when there were no intervals (only one transaction in a group). so i added a safeguard when calculating the average interval to handle cases with single transactions in a group.

### 6. Flexible Monthly Patterns

Some monthly transactions didn't fall exactly 30 days apart. so i implemented a more flexible check for monthly patterns, considering transactions as monthly if at least 75% of the intervals are between 28 and 35 days.


## Usage

1. Place your transaction data in `transactions.json`
2. Run `python main.py`

## Running Tests

Run `python -m unittest discover tests` from the project root.

## Future Improvements

1. Implement more sophisticated pattern recognition algorithms
2. Consider transaction amounts in addition to dates for identifying recurring transactions
3. Use machine learning techniques for more accurate identification
4. Implement a confidence score for each identified recurring transaction


