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

vlan_id = str(sys.argv[1])
vlan_name = str(sys.argv[2])
olc = str(sys.argv[3])
int_id = str(sys.argv[4])
mode = str(sys.argv[5])
sw_vlan = str(sys.argv[6])


if vlan_id and vlan_name:
    commands=[f'vlan {vlan_id}',f'name {vlan_name}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)
if olc:
    commands=[f'no vlan {vlan_id}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)
if mode:
    commands=[]
    if mode == 'access':
        commands=[f'interface {int_id}','switchport mode access', f'switchport access vlan {sw_vlan}']
    else:
        commands=[f'interface {int_id}','switchport trunk encapsulation dot1q','switchport mode trunk', f'switchport trunk allow vlan {sw_vlan}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)
