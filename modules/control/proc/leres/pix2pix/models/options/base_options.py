from .test_options import TestOptions


class BaseOptions(TestOptions):
    def __init__(self):
        # Initialize the options here

    def initialize(self):
        TestOptions.modify_commandline_options(parser, False)
        # Initialize the options here

    # Rest of the code...
