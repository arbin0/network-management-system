from netmiko import ConnectHandler
import sys
import json
import os
import time
import threading

#Checking if the script is running on previous thread or not
pid_file = "pip.pid"
if not os.path.exists(pid_file):
   pass
else:
    with open("pip.pid", "r") as f:
       pid = int(f.read())
       try:
           os.kill(pid,9)
       except:
           pass

cisco ={
    'device_type': 'cisco_ios',
    'host': sys.argv[3],
    'username': sys.argv[1],
    'password': sys.argv[2],
    'secret' : sys.argv[5],
}
type = ''


def run( type ):
    pid = os.getpid()
    with open("pip.pid", "w") as f:
       f.write(str(pid))
    while True:
        print('thread started')
        json_file_path = r'static\data\data.json'
        host_json_path = r'static\data\host_info.json'
        if type == 'router':
            output1 = net_connect.send_command('show interface', use_textfsm=True)
            output2 = net_connect.send_command('show ip route')
            output3 = net_connect.send_command('show version', use_textfsm=True)
            output4 = net_connect.send_command('show ip ospf neighbor')
            output5 = net_connect.send_command('show ip eigrp neighbors')
            output6 = net_connect.send_command('show ip bgp summary')
            output = {'interface': output1, 'route': output2, 'version': output3, 'ospf': output4, 'eigrp': output5, 'bgp': output6, 'device_type': type}
        else:
            output1 = net_connect.send_command('show interface', use_textfsm=True)
            output2 = net_connect.send_command('show interfaces switchport', use_textfsm=True)
            output3 = net_connect.send_command('show version', use_textfsm=True)
            output4 = net_connect.send_command('show spanning-tree')
            output5 = net_connect.send_command('show interfaces trunk')
            output6 = net_connect.send_command('show vlan', use_textfsm=True)
            output = {'interface': output1, 'switchport': output2, 'version': output3, 'spanning': output4, 'trunk': output5, 'vlan': output6, 'device_type': type}


        json_output = json.dumps(output, indent =2)
        json_host = json.dumps(cisco, indent=2)
        with open(json_file_path, "w") as outfile:
            outfile.write(json_output)
        if not os.path.exists(host_json_path):
            with open(host_json_path, 'w'): pass

        with open(host_json_path, "w") as outfile:
            outfile.write(json_host)
        # net_connect.find_prompt()
        if stop_threads:
            break

net_connect = ConnectHandler(**cisco)
stop_threads =False
t1 = threading.Thread(target = run, args= (sys.argv[4],))
t1.start()
time.sleep(200)
stop_threads = True
t1.join()
print('thread killed')
