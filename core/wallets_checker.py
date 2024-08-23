from asyncio import Event, Lock, Queue
from collections import defaultdict
from functools import partial
import logging

from playwright.async_api import async_playwright, Browser, Page, Playwright, Response

from core.balance import Balance
from core.utils import save_balances_rows_to_file

logging.basicConfig(level=logging.INFO)


class DebankWalletsChecker:
    def __init__(
            self,
            save_results_to_file: bool = True,
            output_file_path: str = './wallets_balance.txt',
            max_threads: int = 3,
    ):
        self._should_save_to_file: bool = save_results_to_file
        self._output_file_path: str = output_file_path
        self._max_threads: int = max_threads

        self._initialized: Event = Event()
        self._initialization_lock: Lock = Lock()
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._pages_queue: Queue[Page] = Queue()

        self.balance_by_wallet: defaultdict[str, Balance] = defaultdict(Balance)

    async def _initialize_playwright(self) -> None:
        """
        Method to initialize playwright for checker.

        :return: None
        """
        async with self._initialization_lock:
            if self._initialized.is_set():
                return

            logging.info('Initializing debank checker browser...')

            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                ],
            )

            for _ in range(self._max_threads):
                page: Page = await self._browser.new_page()
                await self._pages_queue.put(page)

            self._initialized.set()
            logging.info('Debank checker browser initialized.')

    @staticmethod
    async def _parse_api_response(response: Response) -> list[dict]:
        """
        Parse API response and return a list of dicts from "data" section.

        :param response: Playwright's Response object.
        :return: List of dicts from "data" section.
        """
        response_json: dict = await response.json()

        return response_json['data']

    async def _process_api_request(
            self,
            response: Response,
            wallet: str,
    ) -> None:
        """
        Method to handle API requests with balance data.

        :param response: Response object from Playwright.
        :param wallet: Wallet address string.
        :return: None
        """
        try:
            request_url: str = response.request.url

            if "https://api.debank.com/token/balance_list" in request_url:
                for token in await self._parse_api_response(response):
                    amount: float = token['amount']
                    price: float = token['price']

                    balance: float = amount * price

                    self.balance_by_wallet[wallet].tokens += balance

            elif 'https://api.debank.com/portfolio/project_list?' in request_url:
                for chain in await self._parse_api_response(response):
                    for portfolio_item in chain['portfolio_item_list']:
                        balance: float = portfolio_item['stats']['asset_usd_value']

                        self.balance_by_wallet[wallet].projects += balance

        except Exception:
            pass

    async def check_wallet_balance(self, wallet: str) -> Balance:
        """
        Method to check balance of wallet.

        :param wallet: wallet address to check.
        :return: Balance object.
        """
        if not self._initialized.is_set():
            await self._initialize_playwright()

        page: Page = await self._pages_queue.get()

        handle_api_request_method = partial(
            self._process_api_request,
            wallet=wallet,
        )

        page.on(event='response', f=handle_api_request_method)

        try:
            await page.goto(
                url=f"https://debank.com/profile/{wallet}",
                wait_until='networkidle',
                timeout=30 * 1000,
            ),
        except TimeoutError:
            logging.error(f'Timed out waiting for balance obtain for {wallet}')

        page.remove_listener(event='response', f=handle_api_request_method)

        balance: Balance = self.balance_by_wallet[wallet]
        logging.info(f'{wallet} | {balance}')

        if self._should_save_to_file:
            save_balances_rows_to_file(
                balances=self.balance_by_wallet,
                path=self._output_file_path,
            )

        await self._pages_queue.put(page)

        return balance
