import re
from selectolax.parser import HTMLParser


def parse_title(tree: HTMLParser) -> str:
    node = tree.css_first("#sideTitleTitle")
    return node.text(strip=True) if node else ""

def parse_price_usd(tree: HTMLParser) -> int:
    node = tree.css_first("strong.common-text.ws-pre-wrap.titleL")
    if not node:
        return 0
    text = node.text(strip=True)
    number_str = re.sub(r"[^\d]", "", text)
    return int(number_str) if number_str.isdigit() else 0

def parse_odometer(text: str) -> int:
    try:
        value = float(text.replace("тис.", "").replace("км", "").replace(" ", "").strip())
        return int(value * 1000)
    except:
        return 0

def parse_username(tree: HTMLParser) -> str:
    node = tree.css_first("#sellerInfo .common-text.titleM")
    return node.text(strip=True) if node else ""

def parse_image_url(tree: HTMLParser) -> str:
    img_node = tree.css_first("span.picture picture img")
    if img_node:
        url = img_node.attributes.get("data-src") or img_node.attributes.get("src")
        return url or ""
    return ""

def parse_images_count(tree: HTMLParser) -> int:
    spans = tree.css("span.common-badge span")
    if len(spans) >= 2:
        return int(spans[1].text(strip=True))
    return 0

def parse_car_number(tree: HTMLParser) -> str:
    node = tree.css_first(".car-number.ua span.common-text.ws-pre-wrap.body")
    return node.text(strip=True) if node else ""

def parse_car_vin(tree: HTMLParser) -> str:
    node = tree.css_first("#badgesVin .common-text.ws-pre-wrap.badge")
    return node.text(strip=True) if node else ""

def get_total_pages(tree: HTMLParser) -> int:
    node = tree.css_first("span.page-item.dhide.text-c")
    if not node:
        return 1

    text = node.text(strip=True)
    if "/" in text:
        total_part = text.split("/")[-1]
        digits = "".join(re.findall(r'\d+', total_part))
        return int(digits) if digits else 1

    return 1
