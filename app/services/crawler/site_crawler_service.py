from sqlalchemy.orm import Session

from app.models.analysis_run import AnalysisRun
from app.models.site_page import SitePage
from app.services.crawler.extractor import extract_page_data
from app.services.crawler.http_loader import HtmlLoader


class SiteCrawlerService:
    def __init__(self, db: Session, loader: HtmlLoader | None = None):
        self.db = db
        self.loader = loader or HtmlLoader()

    def crawl_run_primary_page(self, run: AnalysisRun) -> SitePage | None:
        target_url = run.selected_page_url or run.project.website_url
        load = self.loader.fetch(target_url)

        if load.html is None:
            run.error_message = f"crawl failed: {load.error}"
            self.db.commit()
            return None

        extracted = extract_page_data(load.html, load.url)
        page = SitePage(
            run_id=run.id,
            url=load.url,
            title=extracted.title,
            meta_description=extracted.meta_description,
            h1=extracted.h1,
            text_content=extracted.text_content,
            headings=extracted.headings,
            cta_buttons=extracted.cta_buttons,
            phones=extracted.phones,
            forms_count=extracted.forms_count,
            messengers=extracted.messengers,
            has_price=extracted.has_price,
            has_faq=extracted.has_faq,
            has_reviews=extracted.has_reviews,
            page_type=extracted.page_type,
            extracted_json=extracted.to_dict(),
        )
        self.db.add(page)
        self.db.commit()
        self.db.refresh(page)
        return page
