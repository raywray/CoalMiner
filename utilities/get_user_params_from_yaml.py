import yaml

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        params = yaml.safe_load(file)
    return params