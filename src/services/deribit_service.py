import aiohttp


class DeribitService:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"
    index_btc_usdt = {"index_name": "btc_usdt"}
    index_eth_usdt = {"index_name": "eth_usdt"}

    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get_index_price_btc(self):
        async with self.session.get(self.BASE_URL, params=self.index_btc_usdt) as response:
            response.raise_for_status()
            data = await response.json()
            return data["result"]["index_price"]

    async def get_index_price_eth(self):
        async with self.session.get(self.BASE_URL, params=self.index_eth_usdt) as response:
            response.raise_for_status()
            data = await response.json()
            return data["result"]["index_price"]
