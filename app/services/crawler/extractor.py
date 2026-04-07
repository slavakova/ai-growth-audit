import re
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup

PHONE_RE = re.compile(r"(?:\+?\d[\d\s\-()]{7,}\d)")
PRICE_RE = re.compile(r"(?:\$|€|£|₽|usd|eur|руб|price|цена)", re.IGNORECASE)
FAQ_RE = re.compile(r"faq|частые вопросы|вопросы и ответы", re.IGNORECASE)
REVIEWS_RE = re.compile(r"reviews|отзывы|кейсы", re.IGNORECASE)


@dataclass
class ExtractedPageData:
    title: str | None
    meta_description: str | None
    h1: str | None
    text_content: str
    headings: list[str]
    cta_buttons: list[str]
    phones: list[str]
    forms_count: int
    messengers: list[str]
    has_price: bool
    has_faq: bool
    has_reviews: bool
    page_type: str

    def to_dict(self) -> dict:
        return asdict(self)


def _clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.split())
    return cleaned if cleaned else None


def _detect_messengers(html: str) -> list[str]:
    low = html.lower()
    hits: list[str] = []
    mapping = {
        "telegram": ["t.me", "telegram"],
        "whatsapp": ["wa.me", "whatsapp"],
        "viber": ["viber"],
        "facebook_messenger": ["m.me", "messenger"],
    }
    for name, patterns in mapping.items():
        if any(pattern in low for pattern in patterns):
            hits.append(name)
    return hits


def _detect_page_type(url: str, headings: list[str], text: str) -> str:
    low_url = url.lower()
    low_text = (" ".join(headings) + " " + text[:1000]).lower()
    if any(token in low_url for token in ["/blog", "/article", "/news"]) or "читать" in low_text:
        return "article"
    if any(token in low_url for token in ["/catalog", "/products", "/shop"]):
        return "catalog_page"
    if any(token in low_url for token in ["/services", "/service"]) or "услуги" in low_text:
        return "service_page"
    return "landing"


def extract_page_data(html: str, url: str) -> ExtractedPageData:
    soup = BeautifulSoup(html, "html.parser")

    title = _clean_text(soup.title.string if soup.title else None)
    meta = soup.find("meta", attrs={"name": "description"})
    meta_description = _clean_text(meta.get("content") if meta else None)

    h1_tag = soup.find("h1")
    h1 = _clean_text(h1_tag.get_text(" ", strip=True) if h1_tag else None)

    for tag_name in ["script", "style", "noscript"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    text_content = _clean_text(soup.get_text(" ", strip=True)) or ""
    headings = [_clean_text(tag.get_text(" ", strip=True)) or "" for tag in soup.find_all(["h2", "h3"])]
    headings = [h for h in headings if h]

    cta_buttons: list[str] = []
    cta_keywords = ("заказать", "купить", "оставить", "получить", "sign up", "book", "contact", "demo")
    for tag in soup.find_all(["button", "a"]):
        text = (_clean_text(tag.get_text(" ", strip=True)) or "").lower()
        if text and any(word in text for word in cta_keywords):
            cta_buttons.append(text)

    phones = sorted(set(PHONE_RE.findall(text_content)))
    forms_count = len(soup.find_all("form"))
    messengers = _detect_messengers(html)

    has_price = bool(PRICE_RE.search(text_content))
    has_faq = bool(FAQ_RE.search(text_content))
    has_reviews = bool(REVIEWS_RE.search(text_content))
    page_type = _detect_page_type(url, headings, text_content)

    return ExtractedPageData(
        title=title,
        meta_description=meta_description,
        h1=h1,
        text_content=text_content,
        headings=headings,
        cta_buttons=sorted(set(cta_buttons)),
        phones=phones,
        forms_count=forms_count,
        messengers=messengers,
        has_price=has_price,
        has_faq=has_faq,
        has_reviews=has_reviews,
        page_type=page_type,
    )
