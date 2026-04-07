from dataclasses import dataclass

import httpx


@dataclass
class LoadResult:
    url: str
    html: str | None
    error: str | None = None
    status_code: int | None = None


class HtmlLoader:
    def __init__(self, timeout_seconds: float = 10.0, max_retries: int = 2) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def fetch(self, url: str) -> LoadResult:
        last_error: str | None = None
        for _ in range(self.max_retries + 1):
            try:
                with httpx.Client(timeout=self.timeout_seconds, follow_redirects=True) as client:
                    response = client.get(url)
                    if response.status_code >= 400:
                        return LoadResult(url=url, html=None, status_code=response.status_code, error="HTTP error")
                    return LoadResult(url=str(response.url), html=response.text, status_code=response.status_code)
            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as exc:
                last_error = str(exc)
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                break
        return LoadResult(url=url, html=None, error=last_error or "Failed to load URL")
