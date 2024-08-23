import argparse
import asyncio

from core.wallets_checker import DebankWalletsChecker
from core.utils import get_wallets_from_file


async def main(
        wallets_file_path: str,
        results_file_path: str,
        max_threads: int,
):
    debank_checker = DebankWalletsChecker(
        output_file_path=results_file_path,
        max_threads=max_threads,
    )

    await asyncio.gather(
        *[
            debank_checker.check_wallet_balance(wallet)
            for wallet in get_wallets_from_file(
                path=wallets_file_path,
            )
        ]
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Debank Wallet Balance Checker")

    parser.add_argument(
        '-wallets',
        type=str,
        help="Path to the file containing wallet addresses (default: wallets.txt)",
        default='wallets.txt',
    )
    parser.add_argument(
        '-output',
        type=str,
        help="Path to the file where results will be saved (default: balances.txt)",
        default='balances.txt',
    )
    parser.add_argument(
        '--max_threads',
        type=int,
        default=5,
        help="Maximum number of parallel threads (default: 5)",
    )

    args = parser.parse_args()

    asyncio.run(
        main(
            wallets_file_path=args.wallets,
            results_file_path=args.output,
            max_threads=args.max_threads,
        ),
    )
