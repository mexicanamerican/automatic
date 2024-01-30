import unittest
from unittest.mock import MagicMock

from modules.control.proc.leres.pix2pix.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.opt = MagicMock()
        self.model = BaseModel(self.opt)

    def test_set_input(self):
        # TODO: Write test cases for the set_input function
        pass

    def test_save_networks(self):
        # TODO: Write test cases for the save_networks function
        pass

    def test_load_networks(self):
        # TODO: Write test cases for the load_networks function
        pass

    def test_print_networks(self):
        # TODO: Write test cases for the print_networks function
        pass

    def test_set_requires_grad(self):
        # TODO: Write test cases for the set_requires_grad function
        pass


if __name__ == '__main__':
    unittest.main()
