from netmiko import ConnectHandler
import sys
import json
import os
host_json_path = r'static\data\host_info.json'
cisco = {}
with open(host_json_path) as json_file:
    data = json.load(json_file)
    cisco = data
net_connect = ConnectHandler(**cisco)
net_connect.enable()
int = sys.argv[1]
ip = sys.argv[2]
mask = sys.argv[3]
ls = sys.argv[4]

if ip and mask:
    commands = [f'interface {int}', f'ip address {ip} {mask}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)

if ls:
    commands = [f'interface {int}', ls]
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)
