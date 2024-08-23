"""
This module defines the `Balance` class, which is used to represent and format financial balances
for tokens and projects. The class provides a simple structure for managing these balances and
a customizable string representation for logging or displaying the current state.

Usage example:
    balance = Balance()
    balance.tokens = 5000.50
    balance.projects = 15000.75
    print(balance)
    # Output: TOTAL: 20,001.25$ | TOKENS: 5,000.50$ | PROJECTS: 15,000.75$
"""


class Balance:
    _repr_template = "TOTAL: {total:,.2f}$ | TOKENS: {tokens:,.2f}$ | PROJECTS: {projects:,.2f}$"

    def __init__(self):
        self.tokens: float = 0.0
        self.projects: float = 0.0

    def __repr__(self):
        total_balance: float = self.tokens + self.projects

        return self._repr_template.format(
            total=total_balance,
            tokens=self.tokens,
            projects=self.projects,
        )
