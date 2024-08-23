"""
This module provides utility functions for the Debank Checker project.
"""
from collections import defaultdict

from core.balance import Balance


def get_wallets_from_file(path: str) -> list[str]:
    """
    Reads the wallets file from disk and returns a list of wallets.

    :return: list of wallets.
    """
    with open(path) as wallets_file:
        return [
            line.strip()
            for line in wallets_file.readlines()
        ]


def save_balances_rows_to_file(
        balances: defaultdict[str, Balance],
        path: str,
) -> None:
    """
    Save wallets balance to given path file.

    :param balances: wallets balances mapping.
    :param path: path to save balances to.
    :return: None
    """
    with open(file=path, mode='w') as file:
        for wallet, balance in balances.items():
            file.write(f'{wallet} | {balance}\n')
