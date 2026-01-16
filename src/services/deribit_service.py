import aiohttp


class DeribitService:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

    def __init__(self):
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_index_price(self, ticker: str) -> float:
        """
        Получает индексную цену для указанного тикера.

        Args:
            ticker: Тикер валюты (например, 'btc_usd' или 'eth_usd')

        Returns:
            Индексная цена валюты

        Raises:
            aiohttp.ClientError: При ошибке HTTP запроса
            KeyError: При отсутствии данных в ответе
        """
        session = await self._get_session()
        index_name = ticker.lower()
        params = {"index_name": index_name}

        async with session.get(self.BASE_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            if "result" not in data or "index_price" not in data["result"]:
                raise ValueError(f"Invalid response format for ticker {ticker}")
            return float(data["result"]["index_price"])
