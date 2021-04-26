#!/usr/bin/env python3

import json
import re
from json import JSONEncoder

re_ingredient = re.compile(r'(?P<name>[\w ]+)(; (?P<subtype>[\w ]+))? (?P<recipe_page_nums>[\d, ]+)')
re_consecutive_whitespace = re.compile(r'\s+')
re_slugify_drop_chars = re.compile(r'[^a-zA-Z0-9 -]')


def slugify(s: str):
    s = re_consecutive_whitespace.sub(' ', s)
    s = re_slugify_drop_chars.sub('', s)
    s = s.lower().replace(' ', '-')
    return s


def normalized_name(name: str):
    name = name.strip()
    name = name.replace('-', ' ')
    name = re_consecutive_whitespace.sub(' ', name)
    name = name.title()
    return name


def normalized_subtype(subtype: str):
    if subtype is None:
        return subtype

    return normalized_name(subtype).lower()


def compute_ingredient_id(name, subtype):
    if subtype:
        return f"{slugify(name)}:{slugify(subtype)}"

    return slugify(name)


def compute_ingredient_search_key(name, subtype):
    if subtype:
        return f"{name} ({subtype})"

    return name


class Ingredient:
    def __init__(self, name, subtype, recipe_page_nums):
        name = normalized_name(name)
        subtype = normalized_subtype(subtype)
        self.id = compute_ingredient_id(name, subtype)
        self.name = name
        self.subtype = subtype
        self.search_key = compute_ingredient_search_key(name, subtype)
        self.recipe_page_nums = recipe_page_nums
        self.recipe_refs = []


class Recipe:
    def __init__(self, source, page_num, name, category):
        self.source = source
        self.source_name = normalized_name(source)
        self.id = f'{self.source}-{page_num}'
        self.page_num = page_num
        self.name = normalized_name(name)
        self.category = normalized_name(category)
        self.ingredients = []


class MyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Ingredient):
            d = o.__dict__.copy()
            del d['recipe_page_nums']
            return d

        return o.__dict__


class InvalidIngredientLine(Exception):
    def __init__(self, line):
        super().__init__(f"line did not match pattern;\n"
                         f"line = {line}"
                         f"pattern = {re_ingredient.pattern}")


def parse_ingredients(source):
    ingredients = []

    with open(f'{source}/ingredients.txt') as fh:
        for line in fh:
            ingredient = parse_ingredient_line(line)
            ingredients.append(ingredient)

    return ingredients


def parse_ingredient_line(line):
    match = re_ingredient.match(line)
    if match is None:
        raise InvalidIngredientLine(line)
    name = match.group('name')
    subtype = match.group('subtype')
    recipe_page_nums = [int(s) for s in match.group('recipe_page_nums').split(', ')]
    assert all(recipe_page_nums[i - 1] < recipe_page_nums[i] for i in range(1, len(recipe_page_nums))), \
        f"{name}:{subtype}, page nums not in ascending order: {recipe_page_nums}"

    return Ingredient(name, subtype, recipe_page_nums)


def parse_recipes(source):
    recipes = []

    with open(f'{source}/recipes.txt') as fh:
        category = None
        for line in fh:
            line = line.rstrip()

            if not category:
                category = line.title()
                continue

            if not line:
                category = None
                continue

            page_num, name = line.split(' ', 1)
            recipe = Recipe(source, int(page_num), name, category)
            recipes.append(recipe)

    recipes.sort(key=lambda x: x.name)

    return recipes


def fill_recipe_ingredients(recipes, ingredients):
    page_num_to_recipe = {r.page_num: r for r in recipes}

    for ingredient in ingredients:
        for page_num in ingredient.recipe_page_nums:
            recipe = page_num_to_recipe[page_num]
            recipe.ingredients.append(ingredient)
            ingredient.recipe_refs.append(recipe.id)

    assert all(x.ingredients for x in recipes)
    assert all(x.recipe_refs for x in ingredients)


def main():
    all_recipes = []
    ingredients_index = {}
    for source in ('detox-smoothies', 'green-smoothies'):
        recipes = parse_recipes(source)
        all_recipes.extend(recipes)

        ingredients = parse_ingredients(source)
        fill_recipe_ingredients(recipes, ingredients)

        for ingredient in ingredients:
            if ingredient.id in ingredients_index:
                ingredients_index[ingredient.id].recipe_refs.extend(ingredient.recipe_refs)
            else:
                ingredients_index[ingredient.id] = ingredient

    wrapped = {
        "recipes": all_recipes,
        "ingredients": sorted(ingredients_index.values(), key=lambda x: x.name),
    }
    print(json.dumps(wrapped, indent=2, cls=MyEncoder))


if __name__ == '__main__':
    main()
