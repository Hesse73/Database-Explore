import json
from django.core.management.utils import get_random_secret_key

setting_json = json.load(open('settings.json', 'r'))
setting_json['secret_key'] = get_random_secret_key()

setting_file = open('dataexplore/settings.py', 'r+')
file_content = setting_file.read()
setting_file.close()

file_content = file_content.replace('SECRET_KEY_GENERATED', setting_json['secret_key'])
file_content = file_content.replace('HOST_NAME', setting_json['host_name'])
file_content = file_content.replace('DB_NAME', setting_json['database']['NAME'])
file_content = file_content.replace('DB_USER', setting_json['database']['USER'])
file_content = file_content.replace('DB_PWD', setting_json['database']['PASSWORD'])
file_content = file_content.replace('DB_HOST', setting_json['database']['HOST'])
file_content = file_content.replace('DB_PORT', setting_json['database']['PORT'])

with open('dataexplore/settings.py', 'w') as setting_file:
    setting_file.write(file_content)
    setting_file.close()
