import asyncio
import aiohttp
from loguru import logger
from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright
from src.database.repositories.car_repository import CarRepository

from scraper.client import fetch
from scraper.parser import CarParser
from scraper.phone import PhoneService
from utils.parsing import get_total_pages
from database.engine import db_helper


class AutoRiaScraper:
    def __init__(self, start_url: str, max_concurrency: int = 3) -> None:
        self.start_url = start_url
        self.sem = asyncio.Semaphore(max_concurrency)
        self.parser = None

    async def start(self) -> None:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            phone_service = PhoneService(browser)
            self.parser = CarParser(phone_service)

            async with aiohttp.ClientSession() as session:
                logger.info("[SCRAPER] Begin collecting data...")
                await self.scrape_pages(session)
            
            await browser.close()
            logger.info("[SCRAPER] Work completed.")

    async def save_car(self, data: dict) -> None:
        async with db_helper.get_db_session() as session:
            repo = CarRepository(session)
            success = await repo.save_car(data)
            if success:
                logger.success(f"[DB] Saved: {data['title']}")
            else:
                logger.debug(f"[DB SKIP] Already existing in DB: {data['url']}")

    async def process_car(self, session: aiohttp.ClientSession, url: str) -> None:
        async with self.sem:
            try:
                html = await fetch(session, url)
                if not html:
                    return
                tree = HTMLParser(html)
                data = await self.parser.parse_car(tree, url)
                
                if data:
                    await self.save_car(data)
            except Exception as e:
                logger.error(f"[PROCESS ERROR] {url}: {e}")

    async def get_car_links(self, session: aiohttp.ClientSession, page_url: str) -> list:
        html = await fetch(session, page_url)
        if not html: return []
        
        tree = HTMLParser(html)
        links = []
        for a in tree.css("a.m-link-ticket"):
            href = a.attributes.get("href")
            if href and href.startswith("https://"):
                links.append(href)
        return list(set(links))

    async def scrape_pages(self, session: aiohttp.ClientSession) -> None:
        first_page_html = await fetch(session, self.start_url)
        if not first_page_html:
            logger.error("Failed to load the start page")
            return

        total_pages = get_total_pages(HTMLParser(first_page_html))
        logger.info(f"[PAGINATION] Total pages: {total_pages}")

        for page in range(1, total_pages + 1):
            page_url = f"{self.start_url}?page={page}"
            logger.info(f"Page processing {page} of {total_pages}")

            car_links = await self.get_car_links(session, page_url)
            if not car_links:
                break

            tasks = [self.process_car(session, link) for link in car_links]
            await asyncio.gather(*tasks, return_exceptions=True)
