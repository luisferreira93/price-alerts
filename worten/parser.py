from db.price import Price


def extract_product_info(card) -> Price:
    """Extracts product name, link, price from a product card and maps it to a PriceDTO."""
    
    # Extract product details from the card
    name_tag = card.find('h3', class_='product-card__name')
    name = name_tag.get_text(strip=True) if name_tag else ""

    link_tag = card.find('a', class_='product-card')
    link = "https://www.worten.pt" + link_tag['href'] if link_tag else ""

    price_tag = card.find('span', class_='price__numbers--bold')
    price = price_tag.get_text(strip=True) if price_tag else ""

    product_dto = Price(
        id="some_unique_id",  
        name=name,
        category="some_category", 
        price=price,
        link=link,
        last_discount="some_discount", 
        last_update="2025-02-03 14:30:00", 
        store="Worten"
    )

    return product_dto