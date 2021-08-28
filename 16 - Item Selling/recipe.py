import requests
import re
from bs4 import BeautifulSoup
import json

URL = 'https://www.allrecipes.com'
ROTD = "Recipe of the Day"

MEASUREMENTS = ['can', 'cans', 'tablespoon', 'tablespoons', 'teaspoon', 'teaspoons', ]


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

    return Recipe(recipe)


class Recipe:
    def __init__(self, recipe):
        self.name = recipe['name']
        self.image = recipe['image']['url']
        self.prep_time = self.extract_time_in_min(recipe['prepTime'])
        self.cook_time = self.extract_time_in_min(recipe['cookTime'])
        self.total_time = self.extract_time_in_min(recipe['totalTime'])
        self.servings = self.extract_servings(recipe['recipeYield'])
        self. ingredients = recipe['recipeIngredient']
        self.instructions = self.extract_steps(recipe['recipeInstructions'])
        self.nutrition = self.extract_nutrition(recipe['nutrition'])

    @staticmethod
    def extract_time_in_min(time):
        match = re.match(r'(P)(\d+)(DT)(\d+)(H)(\d+)(M)', time)
        return 60 * int(match.group(4)) + int(match.group(6))

    """
    do try -- just in case not in servings
    """
    @staticmethod
    def extract_servings(servings):
        match = re.match(r'(\d)( servings)', servings)
        return match.group(1)

    @staticmethod
    def extract_steps(steps):
        return [step['text'].strip() for step in steps]

    @staticmethod
    def extract_nutrition(nutrition):
        if '@type' in nutrition:
            del nutrition['@type']
        return nutrition


if __name__ == '__main__':
    rotd_url = rotd_url()
    rec = get_recipe(rotd_url)

    for key, val in rec.__dict__.items():
        print(key + ": " + str(val))




