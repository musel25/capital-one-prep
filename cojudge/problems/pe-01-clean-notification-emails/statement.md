**The ticket.** An import gives the notification service a list of email addresses. Some addresses are duplicates with different spaces or letter case.

**Why it matters.** If you do not clean the list, one person gets the same email two or three times.

### Your task

Write `clean_emails(emails)`. Return a list of clean addresses.

1. Remove whitespace at the start and the end of each address.
2. Change the letters to lowercase.
3. Skip the address if it is now empty.
4. Skip the address if you already have it.
5. Keep the order in which the addresses first appear. Do not sort.

Do not check if an address is valid. Keep the characters inside an address unchanged: `a.b@c` stays `a.b@c`.

**Constraints:**

- `emails` has 0–1000 strings. Each string has at most 200 ASCII characters.
