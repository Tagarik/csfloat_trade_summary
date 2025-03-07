import aiohttp, logging as log, json

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
            