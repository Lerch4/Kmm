import os
from ruamel.yaml import YAML

config_dir_loc = os.path.join(os.path.dirname(__file__), 'config')

config_file = open(os.path.join(config_dir_loc, 'config.yml'))

yaml = YAML()

yaml.allow_duplicate_keys = True

config = yaml.load(config_file)

