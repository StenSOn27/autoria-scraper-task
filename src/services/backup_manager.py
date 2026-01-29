import asyncio
import os
from datetime import datetime
from loguru import logger
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

class BackupManager:
    def __init__(self, dump_dir: str = "dumps") -> None:
        self.dump_dir = dump_dir
        if not os.path.exists(self.dump_dir):
            os.makedirs(self.dump_dir)

    async def create_dump(self) -> None:
        timestamp = datetime.now()
        filename = f"dump_{timestamp}.sql"
        filepath = os.path.join(self.dump_dir, filename)
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASSWORD

        command = [
            "pg_dump",
            "-h", DB_HOST,
            "-p", str(DB_PORT),
            "-U", DB_USER,
            "-d", DB_NAME,
            "-f", filepath,
            "-F", "p"
        ]

        try:
            logger.info(f"[BACKUP] Starting DB dump to {filename}...")
            process = await asyncio.create_subprocess_exec(
                *command,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            _, stderr = await process.communicate()

            if process.returncode == 0:
                logger.success(f"[BACKUP] Successfully saved to {filepath}")
            else:
                logger.error(f"[BACKUP ERROR] {stderr.decode()}")
                
        except Exception as e:
            logger.error(f"[BACKUP CRITICAL] Failed to create dump: {e}")