import asyncio
import re
from playwright.async_api import Browser, BrowserContext
from playwright_stealth.stealth import Stealth
from loguru import logger


class PhoneService:
    def __init__(self, browser: Browser) -> None:
        self.browser = browser

    @staticmethod
    def _normalize_phone(digits: str) -> int | None:
        if len(digits) == 10 and digits.startswith("0"):
            return int("38" + digits)
        elif len(digits) == 12 and digits.startswith("380"):
            return int(digits)
        return None

    async def get_phone(self, url: str) -> int | None:
        context: BrowserContext = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 900}
        )
        page = await context.new_page()

        await page.route("**/*.{png,jpg,jpeg,svg,woff2}", lambda route: route.abort())
        await Stealth().apply_stealth_async(page)

        try:
            logger.info(f"[PHONE SERVICE] Loading {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            await page.evaluate("""() => {
                const adsSelectors = ['.popup', '.overlay', '.ReactModal__Overlay', '#gdpr', '.js-closable-ext', '.advertising'];
                adsSelectors.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));
                document.querySelectorAll('*').forEach(el => {
                    if (window.getComputedStyle(el).getPropertyValue('position') === 'fixed') el.remove();
                });
            }""")

            await asyncio.sleep(0.5)

            btn_main = "button.size-large.conversion"
            await page.wait_for_selector(btn_main, timeout=10000, state="attached")
            await page.click(btn_main, force=True)

            phone_selectors = [
                "a[href^='tel:']",
                ".action-wrapper-link",
                "span.common-text.ws-pre-wrap.action",
            ]

            result_phone = ""
            for _ in range(25):
                for selector in phone_selectors:
                    elements = await page.locator(selector).all()
                    for el in elements:
                        text = await el.inner_text()
                        digits = "".join(re.findall(r"\d+", text))
                        result_phone = self._normalize_phone(digits)
                        if result_phone: break
                    if result_phone: break
                if result_phone: break
                await asyncio.sleep(0.4)

            if not result_phone:
                link_node = page.locator("a[href^='tel:']").first
                if await link_node.count() > 0:
                    href = await link_node.get_attribute("href")
                    digits = "".join(re.findall(r"\d+", href))
                    result_phone = self._normalize_phone(digits)

            if result_phone:
                logger.info(f"[PHONE SUCCESS] {result_phone}")
                return result_phone

            logger.warning(f"[PHONE SKIP] Not found for {url}")
            return None

        except Exception as e:
            logger.error(f"[PHONE ERROR] {url} -> {e}")
            return None
        finally:
            await context.close()
