import unittest
from unittest.mock import MagicMock

from modules.control.proc.leres.pix2pix.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.base_model = BaseModel(None)

    def test_load_networks(self):
        # Mock the necessary objects
        epoch = 1
        self.base_model.model_names = ['net1', 'net2']
        self.base_model.save_dir = '/path/to/save_dir'
        self.base_model.device = 'cuda:0'
        self.base_model.netnet1 = MagicMock()
        self.base_model.netnet2 = MagicMock()

        # Mock the torch.load function
        torch_load_mock = MagicMock()
        torch_load_mock.return_value = {
            'netnet1': MagicMock(),
            'netnet2': MagicMock()
        }
        with unittest.mock.patch('torch.load', torch_load_mock):
            self.base_model.load_networks(epoch)

        # Assert that the state_dict is loaded correctly for each network
        self.base_model.netnet1.load_state_dict.assert_called_once_with(torch_load_mock.return_value['netnet1'])
        self.base_model.netnet2.load_state_dict.assert_called_once_with(torch_load_mock.return_value['netnet2'])

    def test_print_networks(self):
        # Mock the necessary objects
        self.base_model.model_names = ['net1', 'net2']
        self.base_model.netnet1 = MagicMock()
        self.base_model.netnet2 = MagicMock()

        # Mock the print function
        print_mock = MagicMock()
        with unittest.mock.patch('builtins.print', print_mock):
            self.base_model.print_networks(verbose=True)

        # Assert that the network architecture is printed for each network
        self.base_model.netnet1.assert_called_once_with()
        self.base_model.netnet2.assert_called_once_with()

        # Assert that the total number of parameters is printed for each network
        self.assertEqual(print_mock.call_count, 3)  # One for the architecture and two for the total number of parameters

if __name__ == '__main__':
    unittest.main()
