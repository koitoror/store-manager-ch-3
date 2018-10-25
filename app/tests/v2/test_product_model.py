import unittest

from app.tests.base import BaseTestCase

from app.api.models.user import User
from app.api.models.product import Product


class TestProductModel(BaseTestCase):

    def test_get_product_by_id(self):
        User.create_user(self.cursor, "kamardaniel", "kamar@gmail.com", "password")
        Product.add_product(self.cursor, "first product model test", "testing is very essential", 1)
        result = Product.get_product_by_id(self.dict_cursor, 1)
        self.assertIn("first product model test", result.values())

    def test_get_all_products(self):
        User.create_user(self.cursor, "kamardaniel", "kamar@gmail.com", "password")
        Product.add_product(self.cursor, "first product model test", "testing is very essential", 1)
        result = Product.get_all(self.dict_cursor, 1)
        self.assertIn("first product model test", result[0].values())


if __name__ == '__main__':
    unittest.main()