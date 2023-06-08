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

hostname = sys.argv[1]
olc = sys.argv[2]
ospf_id = sys.argv[3]
onetwork = sys.argv[4]
omask = sys.argv[5]
oarea = sys.argv[6]
eigrp_id = sys.argv[7]
enetwork = sys.argv[8]
emask = sys.argv[9]
bgp_id = sys.argv[10]
bgpn = sys.argv[11]
ras = sys.argv[12]
if olc:
    commands =[olc]
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)

if hostname:
    commands=[f'hostname {hostname}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)

if ospf_id:
    commands=[f'router ospf {ospf_id}',f'network {onetwork} mask {omask} area {oarea}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)

if eigrp_id:
    commands=[f'router eigrp {eigrp_id}',f'network {enetwork} mask {emask}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)

if bgp_id:
    commands=[f'router bgp {bgp_id}',f'neighbor {bgpn} remote-as {ras}']
    output = net_connect.send_config_set(commands)
    output += net_connect.send_command("copy run start")
    print(output)
