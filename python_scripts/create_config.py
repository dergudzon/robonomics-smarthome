from requests import get
from ast import literal_eval
import yaml

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIyMjNhNTZkM2JlYWY0ZDc3YjQzZTMxYzQxYTEyNzg4MSIsImlhdCI6MTYzNzIzMTUyNiwiZXhwIjoxOTUyNTkxNTI2fQ.1tv7bpC_1zqNQzLit-TENLiaTbN3kAMR192QA8oLvLc"
light_fields = ['rgb_color', 'brightness', 'effect']
filename = "configuration1.yaml"
start_text = """
default_config:

tts:
  - platform: google_translate
group: !include groups.yaml
script: !include scripts.yaml
scene: !include scenes.yaml

"""
light_parameters = ['brightness', 'rgb_color', 'effect']

def write_config_start(config, filename, start_text):
    with open(filename, "w") as f:
        f.write(start_text)
    if 'automation' not in config:
        config['automation'] = []
    if 'shell_command' not in config:
        config['shell_command'] = {}
    return config

def write_config_automation(config, entity_id, services):
    entity_name = entity_id.split('.')[1]
    entity_domain = entity_id.split('.')[0]
    send_datalog_automation = {'alias': f'send_datalog_{entity_name}', 
            'trigger': {'platform': 'state', 'entity_id': [entity_id]}, 
            'action': {'service': f'shell_command.send_datalog_{entity_name}'}}
    config['automation'].append(send_datalog_automation)
    config['shell_command'][f'send_datalog_{entity_name}'] = f'python3 python_scripts/send_datalog.py {entity_name}={{{{ states("{entity_id}") }}}}'

    for domain in services:
        if domain['domain'] == entity_domain:
            for service in domain['services']:
                if (domain['domain'] == 'light') and (service == 'turn_on'):
                    for parameter in light_parameters:
                        if parameter == 'rgb_color':
                            parameter_data = '[{{ trigger.json.r }}, {{ trigger.json.g }}, {{ trigger.json.b }}]'
                        else:
                            parameter_data = f'{{{{ trigger.json.{parameter} }}}}'
                        control_automation = {'alias': f'{entity_name}_{service}_{parameter}', 
                                    'trigger': {'platform': 'webhook', 'webhook_id': f'{entity_name}_{service}'}, 
                                    'action': {'service': service, 'target': {'entity_id': [entity_id]}, 'data': {f'{parameter}': parameter_data}}}
                        config['automation'].append(control_automation)
                control_automation = {'alias': f'{entity_name}_{service}', 
                                    'trigger': {'platform': 'webhook', 'webhook_id': f'{entity_name}_{service}'}, 
                                    'action': {'service': service, 'target': {'entity_id': [entity_id]}}}
                config['automation'].append(control_automation)
    return config

                

def get_entities():
    url = "http://[200:c98b:ac56:426a:2c7:c209:c413:3d28]:8123/api/states"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }

    response = get(url, headers=headers)
    text = response.text
    text = text.replace('true', '"true"')
    text = text.replace('false', '"false"')
    text = text.replace('null', '"null"')
    text = literal_eval(text)
    return text

def get_services():
    url = "http://[200:c98b:ac56:426a:2c7:c209:c413:3d28]:8123/api/services"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }

    response = get(url, headers=headers)
    text = response.text
    text = text.replace('true', '"true"')
    text = text.replace('false', '"false"')
    text = text.replace('null', '"null"')
    text = literal_eval(text)
    return text

entities = get_entities()
services = get_services()
print(services[25])

print("Available entities:")
for entity in entities:
    print(f"{entity['attributes']['friendly_name']}, id: {entity['entity_id']}")
print()
print("Choose all entitties you want to communicate with through Robonomics and write its ids separated by commas")
print("For example: vacuum.robot_vacuum, sensor.temperature_sensor_temperature, sensor.temperature_sensor_humidity")
entities_to_connect = input()
entities_to_connect = entities_to_connect.split(',')

try:
    with open(filename, "r") as stream:
        config_file = yaml.safe_load(stream)
except:
    config_file = {}

config_file = write_config_start(config_file, filename, start_text)

for entity in entities_to_connect:
    entity = entity.strip()
    config_file = write_config_automation(config_file, entity, services)

with open(filename, "a") as f:
    yaml.dump(config_file, f, default_flow_style=False)



