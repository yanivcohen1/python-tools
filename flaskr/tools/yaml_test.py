import os
import yaml

currentDir = os.path.join(os.path.dirname(__file__))
with open(currentDir + '/config_dev.yml', 'r') as file:
    prime_service = yaml.safe_load(file)

print(prime_service['rest']['url'])
