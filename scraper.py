import requests
from bs4 import BeautifulSoup
from config import BASE_URL, URLL, MAIN_URL

def fetch_recipe_links():
    r = requests.get(BASE_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('div', {'class': 'recipe__nav--view'})
    links = [a_tag['href'] for a_tag in table.find_all('a', href=True)]
    return links

def scrape_recipe_data(link):
    link_r = requests.get(URLL + link)
    link_soup = BeautifulSoup(link_r.text, 'html.parser')
    link_table = link_soup.find('div', {'class': 'box-container'})
    link_tbl = link_soup.find('section', {'class': 'section'})

    if link_table is None:
        return None

    # Recipe name
    name = link_table.find('a', {'class': 'box__title'}).text.strip()

    # Main category
    category = extract_main_category()

    # Subcategory
    subcategory = link_tbl.find('h1', {'class': 'mainLeftSpace'}).text.strip() if link_tbl else None

    # Image URL
    image = URLL + link_table.find('img')['src'] if link_table.find('img') else None

    # Short description
    description = link_table.find('div', {'class': 'box__desc'}).text.strip() if link_table.find('div', {'class': 'box__desc'}) else None

    # Author name
    author = link_table.find('div', {'class': 'name'}).text.strip() if link_table.find('div', {'class': 'name'}) else None

    # Extract sub-links and append to list
    links_for_receipts = []
    if link_table is not None:
        sub_links = link_table.find_all('a', href=True)
        if sub_links:
            href = sub_links[0]['href']
            if href.startswith('/'):
                full_link = URLL + href
                links_for_receipts.append(full_link)

    # Iterate over sub-links and scrape details
    for sub_link in links_for_receipts:
        sub_r = requests.get(sub_link)
        sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
        
        # Portion
        portion = extract_portion(sub_soup)

        # Ingredients
        products = extract_ingredients(sub_soup)

        # Preparation stages
        stages = extract_stages(sub_soup)

        return {
            'რეცეპტის დასახელება': name,
            "რეცეპტის მისამართი": URLL + link,
            'რეცეპტის მთავარი კატეგორიის დასახელება და მისამართი': {'title': category, 'url': BASE_URL},
            'რეცეპტის ქვეკატეგორიის დასახელება და მისამართი': {'title': subcategory, 'url': []},
            'მთავარი სურათის მისამართი': image,
            'მოკლე აღწერა': description,
            "ავტორი სახელი": author,
            "ულუფების რაოდენობა": portion,
            "რეცეპტის ინგრედიენტები": products,
            "რეცეპტის მომზადების ეტაპები": stages
        }

def extract_main_category():
    main_r = requests.get(MAIN_URL)
    main_soup = BeautifulSoup(main_r.text, 'html.parser')
    main_table = main_soup.find('div', {'class': 'recipe__nav--view'})
    
    if main_table:
        info_category = main_table.find_all('a', {'class': 'recipe__nav-item'})
        title = info_category[2]
        ctgr = title.find('div', {'class': 'txt'})
        return ctgr.text.strip() if ctgr else None
    return None

def extract_portion(link_soup):
    info_portion = link_soup.find('div', {'class': 'lineDesc'})
    if info_portion:
        text_parts = info_portion.text.split('\n')
        cleaned_parts = [part.strip() for part in text_parts if part.strip()]
        return cleaned_parts[1] if len(cleaned_parts) > 1 else None
    return None

def extract_ingredients(link_soup):
    info_products = link_soup.find('div', {'class': 'list'})
    products = []
    if info_products:
        pr = info_products.find_all('div', {'class': 'list__item'})
        for product in pr:
            product_text = ' '.join(product.stripped_strings)
            product_text = product_text.replace('\xa0', '')
            product_text = ' '.join(product_text.split())
            if product_text:
                products.append(product_text.strip())
    return products

def extract_stages(link_soup):
    info_stages = link_soup.find('div', {'class': 'lineList'})
    stages = []
    if info_stages:
        st = info_stages.find_all('div', {'class': 'lineList__item'})
        for stage in st:
            stage_text = ' '.join(stage.stripped_strings).strip()
            stages.append(stage_text)
    return stages
