#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'remiarnaud'

import os
import batconf

if __name__ == '__main__':
    print("Vous démarez MeshOui via le script de configuration\n\n")
    os.system("modprobe batman-adv")
    nbr = len(batconf.mesh_interfaces)
    for interface in batconf.mesh_interfaces:
        # if interface exist
        os.system("ifconfig %s down" % interface)
        os.system("ifconfig %s mtu 1532" % interface)
        os.system("iwconfig %s mode ad-hoc essid %s ap 02:12:34:56:78:9A channel 1" % (interface, batconf.network_name))
        os.system("batctl if add %s" % interface)
        os.system("ifconfig %s up" % interface)
        # else print error

    # if nbr == 0:
        # finish

    # if bridge interface
    os.system("brctl addbr mesh-bridge")
    for interface in batconf.bridge_interfaces:
        os.system("brctl addif mesh-bridge %s" % interface)
    os.system("brctl addif mesh-bridge bat0")
    for interface in batconf.bridge_interfaces:
        os.system("ifconfig %s up" % interface)
    os.system("ifconfig bat0 up")
    os.system("ifconfig mesh-bridge up")

    # ask for IP adresse on mesh
    # ask for IP adresse for bridges


