from os import path
from pathlib import Path
from ruamel.yaml import YAML

config_loc = path.join(Path(__file__).parents[1], 'config', 'config.yml')

# config_loc = open(path.join(path.dirname(__file__),'config', 'config.yml'))

with open(config_loc) as config_file:

    yaml = YAML()

    yaml.allow_duplicate_keys = True

    config = yaml.load(config_file)

