import aiohttp, logging as log, json, time

class CSFloat:
    def __init__(self, token: str):
        self.token = token
        self.baseURL = "https://csfloat.com"

    async def requestTradeData(self, role: str, page: int):
        apiEndpoint = '/api/v1/me/trades'
        params = {
            'role': role,
            'state': 'verified',
            'limit': 50,
            'page': page
        }
        headers = {
            'Cookie': f'session={self.token}',
            'Content-Type': 'application/json',
            'accept': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.baseURL + apiEndpoint, headers=headers, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                log.error(f"Error: {e}")
                return None
            
class Currencies:
    def __init__(self):
        self.baseURL = "https://api.exchangerate-api.com/v4/latest/USD"
        self.currencies = None

    async def fetchCurrencies(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.baseURL) as response:
                    response.raise_for_status()
                    self.currencies = await response.json()
            except aiohttp.ClientError as e:
                log.error(f"Error: {e}")
                return None

    def convertCurrency(self, amount: float, currency: str):
        if self.currencies is None:
            return None
        return amount * self.currencies['rates'][currency]