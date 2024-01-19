from .base_options import BaseOptions


class TestOptions(BaseOptions):
    def initialize(self):
        BaseOptions.initialize(self)
        # Add any additional options specific to testing
        self.parser.add_argument('--num_test', type=int, default=100, help='number of test samples')
        self.parser.add_argument('--results_dir', type=str, default='./results', help='directory to save test results')

        # Override any default options for testing
        self.parser.set_defaults(phase='test')

        # Modify any options specific to testing
        self.is_train = False

        # Parse the options
        self.parse()
