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


hostname = sys.argv[1]
olc = sys.argv[2]
oarea = sys.argv[3]
bgp_id = sys.argv[4]
bgpn = sys.argv[5]
ras = sys.argv[6]
oint= sys.argv[7]
bgpg= sys.argv[8]
if olc:
    config_commands = [olc]
    output = net_connect.send_config_set(config_commands, exit_config_mode=False)
    output = net_connect.commit()
    print(output)

if hostname:
    config_commands=[f'set system host-name {hostname}']
    output = net_connect.send_config_set(config_commands, exit_config_mode=False)
    output = net_connect.commit()
    print(output)

if oint:
    config_commands=[f'set protocols ospf area {oarea} interface {oint}']
    output = net_connect.send_config_set(config_commands, exit_config_mode=False)
    output = net_connect.commit()
    print(output)

if bgp_id:
    config_commands=[f'set routing-options autonomous-system {bgp_id}', f'edit protocols bgp group {bgpg}',f'set neighbor {bgpn} peer-as {ras}']
    output = net_connect.send_config_set(config_commands)
    output = net_connect.commit()
    print(output)
