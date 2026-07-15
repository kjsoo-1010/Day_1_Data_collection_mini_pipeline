import httpx

from .config import TIMEOUT, WEATHER_URL


async def fetch_weather(client: httpx.AsyncClient) -> dict:
    resp = await client.get(WEATHER_URL, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
