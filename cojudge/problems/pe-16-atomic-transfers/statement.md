A balance service must apply each transfer without a partial debit or credit.

Implement `apply_transfers(balances, transfers)`. `balances` maps account names to integer cents. Each transfer has `from`, `to`, and `amount`. Process transfers in input order.

Accept only when both accounts exist and the source has at least `amount` cents. Debit the source and credit the target together. A self-transfer requires sufficient funds and leaves the balance unchanged. Reject other transfers without changing balances or creating accounts.

Return `{'accepted': [...], 'balances': {...}}` with one boolean per transfer and every final account balance. Empty inputs are valid.

**Constraints:**

- 0–300 accounts and 0–300 transfers. All required fields are present.
- Account names are nonempty ASCII strings of at most 80 characters.
- Initial balances are integers from 0 to 1000000000000 cents; amounts are integers from 1 to 1000000000000 cents.
- Do not change input objects or their nested values. Each call starts with fresh state.
