from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import admin
from .models import IpList
from subprocess import run,PIPE
import sys
import json
import subprocess
import os
import time
import ipaddress


def home(request):

    if request.user.is_authenticated:
        iplists = IpList.objects.values('ipList','hostname','ios','device_type')
        ip = {"lists" : iplists}
        host_ip='10.1.1.2'
        out= subprocess.Popen([sys.executable,'alert.py',str(host_ip)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return render(request, 'base/base.html', ip)
    else:
        return HttpResponseRedirect("accounts/login")

# def login(request):
#     return render(request, 'login/login.html')
def devicelogin(request, ip, type, ios):
    return render(request, 'devices/devicelogin.html',{'ip': ip, 'type' : type, 'ios':ios})
def switch():
    return render(request, 'devices/devicelogin.html')

################################################################################################################################################################
def backupConf(request):
    device = request.POST.get('device')
    out = subprocess.Popen([sys.executable,'backupConfig.py',device],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if device =='juniper':
        return render(request, 'devices/juniper.html')
    elif device =='cisco_router':
        return render(request, 'devices/device.html')
    elif device =='cisco_switch':
        return render(request, 'devices/switches.html')
##############################################################################################################################
def swconfChange(request):
    ip = request.POST.get('ip')
    mask = request.POST.get('mask')
    ls = request.POST.get('ls')
    int = request.POST.get('intid')
    json_file_path = r'static\data\data.json'
    if request.method == 'GET':
        olc=''
        vlan_id=''
        vlan_name=''
        int_id=''
        mode=''
        sw_vlan=''
        hostname = request.GET.get('hostname')
        dlc = request.GET.get('olc')

        if request.GET.get('olc'):
            dlc = request.GET.get('olc')
        if request.GET.get('hostname'):
            hostname = request.GET.get('hostname')
        if request.GET.get('vlan_id'):
            vlan_id = request.GET.get('vlan_id')
        if request.GET.get('vlan_name'):
            vlan_name = request.GET.get('vlan_name')
        if request.GET.get('int_id'):
            int_id = request.GET.get('int_id')
        if request.GET.get('mode'):
            mode = request.GET.get('mode')
        if request.GET.get('sw_vlan'):
            sw_vlan = request.GET.get('sw_vlan')

        if 'remove' in request.GET:
            olc='no vlan'

        if hostname or dlc:
            sout= subprocess.Popen([sys.executable,'routerconf.py',str(hostname),str(dlc)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            with open(json_file_path) as json_file:
                data = json.load(json_file)
            return render(request, 'devices/switches.html',data)


        out= subprocess.Popen([sys.executable,'switchconf.py',vlan_id,vlan_name,olc,int_id,mode,sw_vlan],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return render(request, 'devices/switches.html',data)

    try:
        out= subprocess.Popen([sys.executable,'routerint.py',str(int),str(ip),str(mask),str(ls)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return render(request, 'devices/switches.html',data)
    except BaseException as e:
        return render(request, 'devices/devicelogin.html',{'message': e})

################################################################################################################################################################

def confChange(request):
    ip = request.POST.get('ip')
    mask = request.POST.get('mask')
    ls = request.POST.get('ls')
    int = request.POST.get('intid')
    json_file_path = r'static\data\data.json'
    if request.method == 'GET':
        hostname=''
        olc=''
        ospf_id=''
        onetwork=''
        omask=''
        oarea=''
        eigrp_id=''
        enetwork=''
        emask=''
        bgp_id=''
        bgpn=''
        ras = ''
        if request.GET.get('hostname'):
            hostname = request.GET.get('hostname')
        if request.GET.get('olc'):
            olc = request.GET.get('olc')
        if request.GET.get('ospf_id'):
            ospf_id = request.GET.get('ospf_id')
        if request.GET.get('onetwork'):
            onetwork = request.GET.get('onetwork')
        if request.GET.get('omask'):
            omask = request.GET.get('omask')
        if request.GET.get('oarea'):
            oarea = request.GET.get('oarea')
        if request.GET.get('eigrp_id'):
            eigrp_id = request.GET.get('eigrp_id')
        if request.GET.get('enetwork'):
            enetwork = request.GET.get('enetwork')
        if request.GET.get('emask'):
            emask = request.GET.get('emask')
        if request.GET.get('bgp_id'):
            bgp_id = request.GET.get('bgp_id')
        if request.GET.get('bgpn'):
            bgpn = request.GET.get('bgpn')
        if request.GET.get('ras'):
            ras = request.GET.get('ras')

        out= subprocess.Popen([sys.executable,'routerconf.py',str(hostname),str(olc),str(ospf_id),str(onetwork),str(omask),str(oarea),str(eigrp_id),str(enetwork),str(emask),str(bgp_id),str(bgpn),str(ras)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return render(request, 'devices/device.html',data)

    try:
        out= subprocess.Popen([sys.executable,'routerint.py',str(int),str(ip),str(mask),str(ls)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return render(request, 'devices/device.html',data)
    except BaseException as e:
        return render(request, 'devices/devicelogin.html',{'message': e})

################################################################################################################################################################

def junoconfChange(request):
    ip = request.POST.get('ip')
    int = request.POST.get('intid')
    json_file_path = r'static\data\data.json'
    if request.method == 'GET':
        hostname=''
        olc=''
        oint=''
        oarea=''
        bgp_id=''
        bgpn=''
        bgpg=''
        ras = ''
        if request.GET.get('hostname'):
            hostname = request.GET.get('hostname')
        if request.GET.get('olc'):
            olc = request.GET.get('olc')
        if request.GET.get('oint'):
            oint = request.GET.get('oint')
        if request.GET.get('oarea'):
            oarea = request.GET.get('oarea')
        if request.GET.get('bgp_id'):
            bgp_id = request.GET.get('bgp_id')
        if request.GET.get('bgpn'):
            bgpn = request.GET.get('bgpn')
        if request.GET.get('ras'):
            ras = request.GET.get('ras')
        if request.GET.get('bgpg'):
            bgpg = request.GET.get('bgpg')



        out= subprocess.Popen([sys.executable,'junoconf.py',str(hostname),str(olc),str(oarea),str(bgp_id),str(bgpn),str(ras),str(oint),str(bgpg)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return render(request, 'devices/juniper.html',data)

    try:
        out= subprocess.Popen([sys.executable,'junoint.py',str(int),str(ip)],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        return render(request, 'devices/juniper.html',data)
    except BaseException as e:
        return render(request, 'devices/devicelogin.html',{'message': e})
##############################################################################################################################################################

def sshLogin(request):
    username = request.POST.get('username')
    password = request.POST.get('pass')
    secret = ''
    ip = request.POST.get('ip')
    type = request.POST.get('type')
    ios = request.POST.get('ios')
    if request.POST.get('secret'):
        secret = request.POST.get('secret')
    json_file_path = r'static\data\data.json'
    host_json_path = r'static\data\host_info.json'
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w'): pass

    if request.method == 'GET':
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            return JsonResponse(data)
    try:
        if ios == 'cisco':
            out= subprocess.Popen([sys.executable,'sshLogin.py',username,password,ip,type,secret],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            out= subprocess.Popen([sys.executable,'junosLogin.py',username,password,ip],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w'): pass
        with open(json_file_path) as json_file:
            data = json.load(json_file)
        time.sleep(8)
        if ios =='junos':
            return render(request, 'devices/juniper.html',data)
        else:
            if type == 'router':
                return render(request, 'devices/device.html',data)
            else:
                return render(request, 'devices/switches.html',data)
    except Exception as e:
        return render(request, 'devices/devicelogin.html',{'message': e})


################################################################################################################################################################


def device(request):
    return render(request, 'devices/device.html')
def audit(request):
    return render(request, 'audit/audit.html')
