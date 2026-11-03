**The ticket.** The balance service moves money between accounts. Each transfer changes two balances.

**Why it matters.** Money must never be lost or created. Either both changes happen, or neither happens. This is called an atomic change. Check everything first, then change.

### Your task

Write `apply_transfers(balances, transfers)`. `balances` maps account names to integer cents. Each transfer has `from`, `to`, and `amount`. Process the transfers in order.

1. Accept a transfer only if both accounts exist and the source has at least `amount` cents.
2. If you accept it, subtract the amount from the source and add it to the target.
3. If you reject it, change nothing and do not create accounts.
4. A transfer to the same account needs enough money. It does not change the balance.

Return `{'accepted': [...], 'balances': {...}}`, with one boolean for each transfer and the final balance of every account. Do not change the input.

**Constraints:**

- 0–300 accounts and 0–300 transfers. Balances and amounts are integers. Amounts are 1 or more.
