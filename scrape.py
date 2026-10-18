# Background me nahi chal aha --improve autoscroll or find another approach
# current approach -> playwright open browser and website -> network connection se fetch api se text extract

import asyncio
import csv
from playwright.async_api import async_playwright

def Url(product_url):
    if "/p/" in product_url and "/product-reviews/" not in product_url:
        product_url = product_url.replace("/p/", "/product-reviews/")
    return product_url


async def scrape_reviews(url):
    reviews = {}
    pending_tasks = set()
    response_count = 0

    def find_reviews(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "ProductReviewValue":
                record = {
                    "review_id": obj.get("id"),
                    "name": obj.get("author"),
                    "date": obj.get("created"),
                    "location": obj.get("location"),
                    "rating": obj.get("rating"),
                    "title": obj.get("title"),
                    "text": obj.get("text"),
                }

                key = record["review_id"] or (
                    record["name"],
                    record["date"],
                    record["rating"],
                    record["title"],
                    record["text"],
                )
                reviews[key] = record

            for value in obj.values():
                find_reviews(value)

        elif isinstance(obj, list):
            for value in obj:
                find_reviews(value)

    async def process_response(response):
        try:
            data = await response.json()
            find_reviews(data)
        except Exception:
            # Ignore responses that aren't readable JSON.
            pass

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        def capture_response(response):
            nonlocal response_count

            if "fetch?cacheFirst=false" in response.url:
                response_count += 1
                task = asyncio.create_task(process_response(response))
                pending_tasks.add(task)
                task.add_done_callback(pending_tasks.discard)

        page.on("response", capture_response)

        try:
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)

            # Scroll manually through the page, stopping when it stabilizes.
            stable_rounds = 0
            previous_height = 0
            previous_response_count = 0
            max_scrolls = 40

            for _ in range(max_scrolls):
                await page.evaluate(
                    "() => window.scrollTo(0, document.body.scrollHeight)"
                )
                await page.wait_for_timeout(600)

                height, current_response_count = await page.evaluate(
                    "() => [document.body.scrollHeight, 0]"
                )
                current_response_count = response_count

                if (
                    height == previous_height
                    and current_response_count == previous_response_count
                ):
                    stable_rounds += 1
                else:
                    stable_rounds = 0

                previous_height = height
                previous_response_count = current_response_count

                # Three stable rounds usually means loading has stopped.
                if stable_rounds >= 3:
                    break

            # Finish processing responses already captured.
            while pending_tasks:
                await asyncio.gather(*list(pending_tasks), return_exceptions=True)

        finally:
            await browser.close()

    fields = [
        "review_id", "name", "date", "location",
        "rating", "title", "text"
    ]

    with open(
        "flipkart_reviews.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reviews.values())

    print(f"Extracted {len(reviews)} unique reviews.")
    print("Saved to flipkart_reviews.csv")


if __name__ == "__main__":
    product_url = input("Enter Product URL: ").strip()
    asyncio.run(scrape_reviews(Url(product_url)))
