from app.services.crawler.extractor import extract_page_data


def test_extract_page_data_core_fields() -> None:
    html = """
    <html>
      <head>
        <title>Test Page</title>
        <meta name="description" content="Best services in NY" />
      </head>
      <body>
        <h1>Main Heading</h1>
        <h2>Our Services</h2>
        <h3>FAQ</h3>
        <a href="#">Book a demo</a>
        <button>Заказать звонок</button>
        <p>Call us +1 (555) 444-2211</p>
        <p>Price from $99</p>
        <p>Отзывы клиентов</p>
        <a href="https://t.me/company">Telegram</a>
        <form><input type="text" /></form>
      </body>
    </html>
    """

    data = extract_page_data(html, "https://example.com/services/seo")
    assert data.title == "Test Page"
    assert data.meta_description == "Best services in NY"
    assert data.h1 == "Main Heading"
    assert "Our Services" in data.headings
    assert data.forms_count == 1
    assert data.has_price is True
    assert data.has_faq is True
    assert data.has_reviews is True
    assert "telegram" in data.messengers
    assert data.page_type == "service_page"


def test_extract_page_data_article_page_type() -> None:
    html = "<html><body><h1>Article</h1><p>читать далее</p></body></html>"
    data = extract_page_data(html, "https://example.com/blog/how-to-grow")
    assert data.page_type == "article"
