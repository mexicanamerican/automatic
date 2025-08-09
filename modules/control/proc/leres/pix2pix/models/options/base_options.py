import argparse


class BaseOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.initialized = False

    def initialize(self, parser):
        parser.add_argument('--option1', type=int, default=0, help='Description of option 1')
        parser.add_argument('--option2', type=float, default=0.0, help='Description of option 2')
        # Add more options here

        self.initialized = True

    def parse(self):
        if not self.initialized:
            self.initialize(self.parser)
        self.opt = self.parser.parse_args()

    def print_options(self):
        message = ''
        message += '----------------- Options -----------------\n'
        for k, v in sorted(vars(self.opt).items()):
            message += f'{str(k):>20}: {str(v):<30}\n'
        message += '----------------- End ---------------------'
        print(message)

    def save_options(self, file_path):
        with open(file_path, 'w') as file:
            file.write(self.get_current_options_string())

    def load_options(self, file_path):
        with open(file_path, 'r') as file:
            options_str = file.read()
        self.parse_additional_options(eval(options_str))

    def parse_additional_options(self, additional_args):
        for k, v in additional_args.items():
            setattr(self.opt, k, v)

    def get_current_options(self):
        return vars(self.opt)

    def validate(self):
        # Add validation logic here
        pass

    def get_current_options_string(self):
        message = ''
        for k, v in sorted(vars(self.opt).items()):
            message += f'{str(k)}={str(v)}\n'
        return message
