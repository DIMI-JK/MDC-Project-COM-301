#Background me nahi chal aha --improve autoscroll or fibd another approach
#current approach -> playwright open browser and website -> network connection se fetch api se text extract

import asyncio
import csv
from playwright.async_api import async_playwright

def Url(product_url):
    if "/p/" in product_url and "/product-reviews/" not in product_url:
        product_url = product_url.replace("/p/", "/product-reviews/")
    return product_url

# async def auto_scroll(page, responses, max_idle_rounds=6, max_scrolls=300):
#     idle_rounds = 0
#     last_count = 0

#     # Put the mouse over the page so the wheel events go to the content
#     await page.mouse.move(600, 500)

#     for i in range(max_scrolls):
#         # Real wheel scroll (works for window AND inner scroll containers)
#         await page.mouse.wheel(0, 3000)
#         await page.keyboard.press("End")
#         await page.wait_for_timeout(1500)

#         # Also try scrolling any inner scrollable element to its bottom
#         await page.evaluate("""
#             () => {
#                 document.querySelectorAll('*').forEach(el => {
#                     if (el.scrollHeight > el.clientHeight + 50) {
#                         const s = getComputedStyle(el).overflowY;
#                         if (s === 'auto' || s === 'scroll') {
#                             el.scrollTop = el.scrollHeight;
#                         }
#                     }
#                 });
#                 window.scrollTo(0, document.documentElement.scrollHeight);
#             }
#         """)
#         await page.wait_for_timeout(500)

#         new_count = len(responses)
#         print(f"Scroll {i+1}: {new_count} responses captured")

#         if new_count == last_count:
#             idle_rounds += 1
#             if idle_rounds >= max_idle_rounds:
#                 print("No new content, stopping.")
#                 break
#         else:
#             idle_rounds = 0
#         last_count = new_count


async def scrape_reviews(url):
    reviews = {}
    responses = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Capture matching network responses
        def capture_response(response):
            if "fetch?cacheFirst=false" in response.url:
                responses.append(response)

        page.on("response", capture_response)

        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        # await auto_scroll(page, responses)

        #Scroll to trigger dynamically loaded content
        for _ in range(20):
            await page.evaluate(
                "() => window.scrollTo(0, document.body.scrollHeight)"
            )
            await page.wait_for_timeout(1500) 

        

        # Process the captured JSON responses
        for response in responses:
            try:
                data = await response.json()
            except Exception:
                continue

            def find_reviews(obj):
                if isinstance(obj, dict):
                    # Identify an individual review
                    if obj.get("type") == "ProductReviewValue":
                        review_id = obj.get("id")

                        record = {
                            "review_id": review_id,
                            "name": obj.get("author"),
                            "date": obj.get("created"),
                            "location": obj.get("location"),
                            "rating": obj.get("rating"),
                            "title": obj.get("title"),
                            "text": obj.get("text"),
                        }

                        # Avoid duplicates
                        key = review_id or (
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

            find_reviews(data)

        await browser.close()

    fields = ["review_id", "name", "date", "location", "rating", "title", "text"]

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
    url = input("Enter Product URL: ").strip()
    url=Url(url)
    asyncio.run(scrape_reviews(url))
