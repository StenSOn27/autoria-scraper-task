from scraper.phone import PhoneService
from utils.parsing import (
    parse_car_number, parse_car_vin,
    parse_image_url, parse_images_count,
    parse_odometer, parse_price_usd,
    parse_title, parse_username
)
from selectolax.parser import HTMLParser

class CarParser:
    def __init__(self, phone_service: PhoneService) -> None:
        self.phone_service = phone_service

    async def parse_car(self, tree: HTMLParser, url: str) -> dict:
        title = parse_title(tree)
        price_usd = parse_price_usd(tree)
        username = parse_username(tree)
        image_url = parse_image_url(tree)
        images_count = parse_images_count(tree)
        car_number = parse_car_number(tree)
        car_vin = parse_car_vin(tree)
        odo_node = tree.css_first("#basicInfoTableMainInfo0 .common-text.ws-pre-wrap.body")
        odometer = parse_odometer(odo_node.text()) if odo_node else 0

        phone_number = await self.phone_service.get_phone(url)

        return {
            "url": url,
            "title": title,
            "price_usd": price_usd,
            "odometer": odometer,
            "username": username,
            "phone_number": phone_number,
            "image_url": image_url,
            "images_count": images_count,
            "car_number": car_number,
            "car_vin": car_vin,
        }
