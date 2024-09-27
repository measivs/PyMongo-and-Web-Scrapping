from scraper import fetch_recipe_links, scrape_recipe_data
from mongo_handler import MongoHandler
import threading

def scrape_and_insert(link, mongo_handler):
    recipe_data = scrape_recipe_data(link)
    if recipe_data:
        mongo_handler.insert_recipe(recipe_data)

def main():
    mongo_handler = MongoHandler()
    links = fetch_recipe_links()

    threads = []
    for link in links:
        thread = threading.Thread(target=scrape_and_insert, args=(link, mongo_handler))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

