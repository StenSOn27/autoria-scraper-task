import aiohttp

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"[fetch error] {url} -> {e}")
        return ""
