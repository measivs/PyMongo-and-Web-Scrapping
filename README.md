# Recipe Scraper Project

This project scrapes recipe data from [kulinaria.ge](https://kulinaria.ge) and stores it in a MongoDB database. After storing the recipes, it extracts and prints statistics from the database.

## Features

The scraper fetches the following details from each recipe:
- Name of the recipe
- Recipe URL
- Main category name and URL
- Subcategory name and URL
- Image URL
- Brief description
- Author name
- Number of servings
- List of ingredients
- Cooking stages with descriptions

## Statistics

After the data is stored in MongoDB, the project extracts the following statistics:
1. The average number of ingredients per recipe.
2. The average number of cooking stages per recipe.
3. The recipe with the most servings (including its name and URL).
4. The author who has posted the most recipes.

## Setup and Installation

### Prerequisites
- Python 3.7+
- MongoDB installed and running locally

### Installing Dependencies
Clone the project and install the dependencies:

```bash
git clone https://github.com/yourusername/recipe-scraper.git
cd recipe-scraper
pip install -r requirements.txt
