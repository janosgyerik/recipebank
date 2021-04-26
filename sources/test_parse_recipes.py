import unittest

from parse_recipes import slugify, compute_ingredient_id, compute_ingredient_search_key


class MyTestCase(unittest.TestCase):
    def test_slugify_multi_word_string(self):
        self.assertEqual("acai-berry", slugify('Acai berry'))

    def test_slugify_drops_nonalphanumeric_characters(self):
        self.assertEqual("jims-best", slugify("Jim's best"))

    def test_slugify_drops_repeated_whitespace(self):
        self.assertEqual("acai-berry-jam", slugify('Acai  berry   jam'))

    def test_compute_ingredient_id_without_subtype(self):
        self.assertEqual("acai-berry", compute_ingredient_id("Acai berry", None))

    def test_compute_ingredient_id_with_subtype(self):
        self.assertEqual("acai-berry:sliced-and-diced", compute_ingredient_id("Acai berry", 'sliced and diced'))

    def test_compute_ingredient_search_key_without_subtype(self):
        self.assertEqual("Acai berry", compute_ingredient_search_key("Acai berry", None))

    def test_compute_ingredient_search_key_with_subtype(self):
        self.assertEqual("Acai berry (sliced and diced)", compute_ingredient_search_key("Acai berry", 'sliced and diced'))


if __name__ == '__main__':
    unittest.main()
