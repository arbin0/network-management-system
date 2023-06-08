from pysnmp.hlapi import *
import _thread
import time
import ipaddress
import threading
import sys
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    database="NMS"
)
mycursor = mydb.cursor()
def scanHost( ip):
    hostname=''
    ios=''
    device_type=''
    #This loop iterates over getCmd() function to retrieve errors or the values returned when queries with the SNMP OIDs.
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in getCmd(SnmpEngine(),
                              CommunityData('public'),
                              UdpTransportTarget((str(ip), 161)),
                              ContextData(),
                              #For device's Name
                              ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),
                              # To get Device's object ID
                              ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysObjectID', 0))):

        if errorIndication or errorStatus:
            pass
        else:
            c = 1
            for varBind in varBinds:
                for x in varBind:
                    if c == 2:
                        try:
                            split = str(x).split(".")
                            hostname = split[0]
                            ios = split[1]
                        except:
                            hostname = split[0]
                    elif c == 4:
                        if str(x) == '1.3.6.1.4.1.9.1.1':
                            device_type='router'
                        elif str(x) == '1.3.6.1.4.1.2636.1.1.1.2.108':
                            device_type='router'
                            ios = 'junos'
                        else:
                            device_type='switch'
                    else:
                        pass

                    c = c + 1
            mycursor.execute('INSERT INTO Dissertation_iplist (ipList,hostname,ios,device_type) SELECT * FROM (SELECT "%s", "%s", "%s","%s") AS tmp WHERE NOT EXISTS (SELECT hostname FROM Dissertation_iplist WHERE hostname = "%s") LIMIT 1;'% (ip,hostname,ios,device_type,hostname))
            mydb.commit()



#This function seperates the iP network into single ip addresses and start threads to scan the network.
def ipScanner( net):
    for ip in net:
        split = str(ip).split(".")
        if (str(split[3]) == '0') or (str(split[3]) == '255') :
            continue
        else:
            ta = threading.Thread(target = scanHost, name = 'PrimaryThread',
                                args = (ip, ))
            ta.start()


ipScanner(ipaddress.IPv4Network(sys.argv[1]))
