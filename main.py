from scraper import fetch_recipe_links, scrape_recipe_data
from mongo_handler import MongoHandler

def main():
    mongo_handler = MongoHandler()
    links = fetch_recipe_links()

    for link in links:
        recipe_data = scrape_recipe_data(link)
        if recipe_data:
            mongo_handler.insert_recipe(recipe_data)

if __name__ == '__main__':
    main()
