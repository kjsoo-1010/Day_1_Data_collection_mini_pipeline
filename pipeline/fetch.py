import asyncio

import httpx

from .config import IP_URL, TIMEOUT, WEATHER_URL


async def fetch_weather(client: httpx.AsyncClient) -> dict:
    resp = await client.get(WEATHER_URL, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


async def fetch_ip(client: httpx.AsyncClient) -> dict:
    resp = await client.get(IP_URL, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


async def fetch_all() -> tuple[dict, dict]:
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(
            fetch_weather(client),
            fetch_ip(client),
        )
