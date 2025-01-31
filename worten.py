import asyncio
from bs4 import BeautifulSoup
import nest_asyncio
nest_asyncio.apply()

from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig

def extract_product_info(card):
    """Extracts product name, link, and price from a product card."""
    product = {}

    name_tag = card.find('h3', class_='product-card__name')
    if name_tag:
        product['name'] = name_tag.get_text(strip=True)

    link_tag = card.find('a', class_='product-card')
    if link_tag:
        product['link'] = "https://www.worten.pt" + link_tag['href']

    price_tag = card.find('span', class_='price__numbers--bold')
    if price_tag:
        product['price'] = price_tag.get_text(strip=True)

    return product

async def simple_crawl(url):
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
        product = extract_product_info(card)
        
        if product.get('name') and product.get('link') and product.get('price'):
            products.append(product)

    for product in products:
        print(product)

async def crawl_multiple_urls():
    """Run the crawl for multiple URLs."""
    urls = [
        "https://www.worten.pt/gaming/playstation/consolas/ps5?seller_id=worten-1&lf=seller_id",
        "https://www.worten.pt/tv-video-e-som/tvs?seller_id=worten-1&lf=seller_id",
        "https://www.worten.pt/grandes-eletrodomesticos/maquinas-de-loica/maquinas-de-lavar-loica?seller_id=worten-1&lf=seller_id"
    ]
    
    tasks = [simple_crawl(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(crawl_multiple_urls())
