import unittest

from parse_recipes import slugify, compute_ingredient_id, compute_ingredient_search_key, parse_ingredient_line, \
    InvalidIngredientLine

ACAI_BERRY_CANONICAL = 'Acai berry'


class MyTestCase(unittest.TestCase):
    def test_slugify_multi_word_string(self):
        self.assertEqual("acai-berry", slugify(ACAI_BERRY_CANONICAL))

    def test_slugify_drops_nonalphanumeric_characters(self):
        self.assertEqual("jims-best", slugify("Jim's best"))

    def test_slugify_drops_repeated_whitespace(self):
        self.assertEqual("acai-berry-jam", slugify('Acai  berry   jam'))

    def test_compute_ingredient_id_without_subtype(self):
        self.assertEqual("acai-berry", compute_ingredient_id(ACAI_BERRY_CANONICAL, None))

    def test_compute_ingredient_id_with_subtype(self):
        self.assertEqual("acai-berry:sliced-and-diced", compute_ingredient_id(ACAI_BERRY_CANONICAL, 'sliced and diced'))

    def test_compute_ingredient_search_key_without_subtype(self):
        self.assertEqual(ACAI_BERRY_CANONICAL, compute_ingredient_search_key(ACAI_BERRY_CANONICAL, None))

    def test_compute_ingredient_search_key_with_subtype(self):
        self.assertEqual("Acai berry (sliced and diced)",
                         compute_ingredient_search_key(ACAI_BERRY_CANONICAL, 'sliced and diced'))

    def test_parse_ingredient_line(self):
        line = "dandelion; leafs 22, 24"
        ingredient = parse_ingredient_line(line)
        self.assertEqual("dandelion:leafs", ingredient.id)
        self.assertEqual("Dandelion", ingredient.name)
        self.assertEqual("leafs", ingredient.subtype)
        self.assertEqual([22, 24], ingredient.recipe_page_nums)

    def test_parse_ingredient_line_raises_exception_for_invalid_specs(self):
        invalid = [
            "dandelion; leafs; more 22, 24",
            "dandelion;; leafs 22, 24",
            "dandelion;; leafs 22, 24, foo",
        ]
        for line in invalid:
            self.assertRaises(InvalidIngredientLine, lambda: parse_ingredient_line(line))


if __name__ == '__main__':
    unittest.main()
