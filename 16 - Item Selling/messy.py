import requests
import re
from bs4 import BeautifulSoup
import json

URL = 'https://www.allrecipes.com'
ROTD = "Recipe of the Day"


class Recipe:
    def __init__(self, name, image, prep_time, cook_time, total_time, recipe_yield,
                 recipe_ingredients, recipe_instructions, nutrition):
        self.name = name
        self.image = image
        self.prep_time = self.extract_time_in_min(prep_time)
        self.cook_time = self.extract_time_in_min(cook_time)
        self.total_time = self.extract_time_in_min(total_time)
        self.recipe_yield = recipe_yield
        self.recipe_ingredients = recipe_ingredients
        self.recipe_instructions = recipe_instructions
        self.nutrition = nutrition

    @staticmethod
    def extract_time_in_min(time):
        match = re.match(r'(P)(\d+)(DT)(\d+)(H)(\d+)(M)', time)
        return 60 * int(match.group(4)) + int(match.group(6))


def rotd_url():
    allrecipes = requests.get(url=URL).text
    rotd = allrecipes[allrecipes.find(ROTD):][allrecipes[allrecipes.find(ROTD):].find('href="') + len('href="'):]
    url = rotd[:rotd.find('"')]
    return url


def get_recipe(url):
    recipe_page = requests.get(url=url)
    soup = BeautifulSoup(recipe_page.text, "html.parser")
    res = soup.find('script')
    recipe = json.loads(res.contents[0])[1]

    name = recipe['name']
    image = recipe['image']['url']
    prep_time = recipe['prepTime']
    cook_time = recipe['cookTime']
    total_time = recipe['totalTime']
    recipe_yield = recipe['recipeYield']
    recipe_ingredients = recipe['recipeIngredient']
    recipe_instructions = recipe['recipeInstructions']
    nutrition = recipe['nutrition']

    return Recipe(name, image, prep_time, cook_time, total_time, recipe_yield, recipe_ingredients, recipe_instructions,
                  nutrition)


if __name__ == '__main__':
    rotd_url = rotd_url()
    rec = get_recipe(rotd_url)

    for key, val in rec.__dict__.items():
        print(key + ": " + str(val))


