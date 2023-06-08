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

juniper ={
    'device_type': 'juniper_junos',
    'host': sys.argv[3],
    'username': sys.argv[1],
    'password': sys.argv[2],
}
type = ''


def run():
    pid = os.getpid()
    with open("pip.pid", "w") as f:
       f.write(str(pid))
    while True:
        output={}
        print('thread started')
        json_file_path = r'static\data\data.json'
        host_json_path = r'static\data\host_info.json'

        output1 = net_connect.send_command('show interfaces brief',use_textfsm=True)
        output5= net_connect.send_command('show system uptime | match system')
        output2 = net_connect.send_command('show route')
        output3 = net_connect.send_command('show version', use_textfsm=True)
        output4 = net_connect.send_command('show ospf neighbor')
        output6 = net_connect.send_command('show bgp summary')
        output={}
        out2=[]
        # output = {'interface': output1, 'route': output2, 'version': output3, 'ospf': output4,'uptime':output5, 'bgp': output6}
        for out in output1:
            interface = out['interface']
            cmd = net_connect.send_command(f'show interfaces {interface} brief | match inet')
            int=cmd.split(" ")
            try:
                ip = int[6]
            except:
                ip=''
            out1 ={'interface':interface,'ipaddress':ip,'link_status':out['link_status'],'admin_state':out['admin_state']}
            try:
                out2.append(out1)
            except:
                out2 =[out1,]
        output = {'interface': out2, 'route': output2, 'version': output3, 'ospf': output4,'uptime':output5, 'bgp': output6}
        json_output = json.dumps(output, indent =2)
        json_host = json.dumps(juniper, indent=2)
        with open(json_file_path, "w") as outfile:
            outfile.write(json_output)
        if not os.path.exists(host_json_path):
            with open(host_json_path, 'w'): pass

        with open(host_json_path, "w") as outfile:
            outfile.write(json_host)
        # net_connect.find_prompt()
        if stop_threads:
            break

net_connect = ConnectHandler(**juniper)

stop_threads =False
t1 = threading.Thread(target = run, args= ())
t1.start()
time.sleep(100)
stop_threads = True
t1.join()
print('thread killed')
