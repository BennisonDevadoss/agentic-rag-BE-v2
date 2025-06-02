# https://docs.crawl4ai.com/advanced/multi-url-crawling/

import hashlib
from tempfile import NamedTemporaryFile

from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
)


def hash_content(content: str) -> str:
    return hashlib.md5(content.encode("utf-8")).hexdigest()


async def crawl_urls_task_async(urls: list[str]) -> None:
    md_generator = DefaultMarkdownGenerator(
        options={
            "body_width": 100,
            "escape_html": False,
            "ignore_images": True,
        }
    )
    # browser_config = BrowserConfig(headless=True, verbose=False)

    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        word_count_threshold=10,
        exclude_external_links=True,
        exclude_internal_links=True,
        exclude_external_images=True,
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=urls,
            config=config,
        )

    unique_contents = set()
    unique_markdowns = []

    for result in results:
        if result.success:
            text = result.markdown
            content_hash = hash_content(text)
            if content_hash not in unique_contents:
                unique_contents.add(content_hash)
                unique_markdowns.append(text)

    content = "\n\n".join(unique_markdowns)

    total_characters = len(content)
    if total_characters == 0:
        raise ValueError("Failed to scrape any unique content from the URLs")

    with NamedTemporaryFile(
        delete=False, suffix=".md", mode="w", encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        file_path = tmp.name

    return file_path


if __name__ == "__main__":
    import asyncio

    asyncio.run(crawl_urls_task_async([]))
