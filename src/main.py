import asyncio
import sys
from loguru import logger

from scheduler import AppScheduler
from scraper.crawler import AutoRiaScraper
from services.backup_manager import BackupManager
from config import START_URL

logger.remove()
logger.add(sys.stderr, level="INFO")

async def main() -> None:
    scraper = AutoRiaScraper(START_URL)
    backup_mgr = BackupManager()

    app_scheduler = AppScheduler()

    app_scheduler.add_scraping_job(scraper.start)
    app_scheduler.add_backup_job(backup_mgr.create_dump)
    
    app_scheduler.start()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")

if __name__ == "__main__":
    asyncio.run(main())