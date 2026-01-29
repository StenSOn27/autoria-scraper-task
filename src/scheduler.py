from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from config import SCRAPE_TIME, DUMP_TIME

class AppScheduler:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()

    def add_scraping_job(self, job_func) -> None:
        h, m = map(int, SCRAPE_TIME.split(":"))
        self.scheduler.add_job(
            job_func, 
            'cron', 
            hour=h, 
            minute=m, 
            name="daily_scraping"
        )
        logger.info(f"[SCHEDULER] Scraper task set for {SCRAPE_TIME}")

    def add_backup_job(self, job_func) -> None:
        h, m = map(int, DUMP_TIME.split(":"))
        self.scheduler.add_job(
            job_func, 
            'cron', 
            hour=h, 
            minute=m, 
            name="daily_backup"
        )
        logger.info(f"[SCHEDULER] Backup task set for {DUMP_TIME}")

    def start(self):
        self.scheduler.start()
        logger.info("[SCHEDULER] Scheduler started.")
