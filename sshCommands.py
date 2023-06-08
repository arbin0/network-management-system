from netmiko import ConnectHandler
import sys
import json

with open('host_info.json') as json_file:
    cisco = json.load(json_file)

net_connect = ConnectHandler(**cisco)
output1 = net_connect.send_command('show ip interface brief', use_textfsm=True)
output2 = net_connect.send_command('show ip route', use_textfsm=True)
output3 = net_connect.send_command('show version', use_textfsm=True)
# output2 = net_connect.send_command(sys.argv[4])
# output3 = net_connect.send_command(sys.argv[5])
# for port in output1:
#     if port['ipaddr'] == '10.1.1.1':
#         print(port)
output = {'interface': output1, 'route': output2, 'version': output3}
json_output = json.dumps(output, indent =2)
json_host = json.dumps(cisco, indent=2)
with open("data.json", "w") as outfile:
    outfile.write(json_output)
with open("host_info.json", "w") as outfile:
    outfile.write(json_host)
# net_connect.find_prompt()
