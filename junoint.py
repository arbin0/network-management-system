from netmiko import ConnectHandler
import sys
import json
import os
host_json_path = r'static\data\host_info.json'
juniper = {}
with open(host_json_path) as json_file:
    data = json.load(json_file)
    juniper = data
net_connect = ConnectHandler(**juniper)

int = sys.argv[1]
ip = sys.argv[2]


if ip:
    config_commands = [f'set interfaces {int} unit 0 family inet address {ip}']
    output = net_connect.send_config_set(config_commands, exit_config_mode=False)
    output = net_connect.commit()
    print(output)
