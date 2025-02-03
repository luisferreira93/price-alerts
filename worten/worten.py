import sys
import os

# Add the parent directory to the Python path (to access db_operations)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from bs4 import BeautifulSoup
import nest_asyncio
from typing import List
from db.price import Price
from db.db_operations import connect_db, insert_price
nest_asyncio.apply()
from parser import extract_product_info

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig


async def simple_crawl(url) -> List[Price]:
    """Crawl the given URL and extract product details."""
        
    crawler_run_config = CrawlerRunConfig( 
        cache_mode=CacheMode.BYPASS, 
        wait_for="#filtered-grid > div > div > section > div > div", 
        excluded_tags=["head", "header", "script", "footer"]
    )
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            config=crawler_run_config
        )
    
    soup = BeautifulSoup(result.html, 'html.parser')

    product_cards = soup.find_all('div', class_='product-card--grid-container')

    products = []
    for card in product_cards:
        product = extract_product_info(card)  # Now it will work here, when needed
        
        if product.name and product.link and product.price:
            products.append(product)

    return products


async def crawl_multiple_urls():
    """Run the crawl for multiple URLs."""
    urls = [
        "https://www.worten.pt/gaming/playstation/consolas/ps5?seller_id=worten-1&lf=seller_id",
    ]
    conn = connect_db()
    for url in urls:
        products = await simple_crawl(url)
        for product in products:
            insert_price(conn, product)


def main():
    """Main function to execute the crawling."""
    asyncio.run(crawl_multiple_urls())


if __name__ == "__main__":
    main()  
