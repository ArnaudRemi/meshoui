#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = 'remiarnaud'

from socket import AF_INET, AF_INET6, inet_ntop
from ctypes import (
    Structure, Union, POINTER,
    pointer, get_errno, cast,
    c_ushort, c_byte, c_void_p, c_char_p, c_uint, c_int, c_uint16, c_uint32
)
import ctypes.util
import ctypes
import os

class struct_sockaddr(Structure):
    _fields_ = [
        ('sa_family', c_ushort),
        ('sa_data', c_byte * 14)]

class struct_sockaddr_in(Structure):
    _fields_ = [
        ('sin_family', c_ushort),
        ('sin_port', c_uint16),
        ('sin_addr', c_byte * 4)]

class struct_sockaddr_in6(Structure):
    _fields_ = [
        ('sin6_family', c_ushort),
        ('sin6_port', c_uint16),
        ('sin6_flowinfo', c_uint32),
        ('sin6_addr', c_byte * 16),
        ('sin6_scope_id', c_uint32)]

class union_ifa_ifu(Union):
    _fields_ = [
        ('ifu_broadaddr', POINTER(struct_sockaddr)),
        ('ifu_dstaddr', POINTER(struct_sockaddr))]

class struct_ifaddrs(Structure):
    pass
struct_ifaddrs._fields_ = [
    ('ifa_next', POINTER(struct_ifaddrs)),
    ('ifa_name', c_char_p),
    ('ifa_flags', c_uint),
    ('ifa_addr', POINTER(struct_sockaddr)),
    ('ifa_netmask', POINTER(struct_sockaddr)),
    ('ifa_ifu', union_ifa_ifu),
    ('ifa_data', c_void_p)]

libc = ctypes.CDLL(ctypes.util.find_library('c'))

def ifap_iter(ifap):
    ifa = ifap.contents
    while True:
        yield ifa
        if not ifa.ifa_next:
            break
        ifa = ifa.ifa_next.contents

def getfamaddr(sa):
    family = sa.sa_family
    addr = None
    if family == AF_INET:
        sa = cast(pointer(sa), POINTER(struct_sockaddr_in)).contents
        addr = inet_ntop(family, sa.sin_addr)
    elif family == AF_INET6:
        sa = cast(pointer(sa), POINTER(struct_sockaddr_in6)).contents
        addr = inet_ntop(family, sa.sin6_addr)
    return family, addr

class NetworkInterface(object):
    def __init__(self, name):
        self.name = name
        self.index = libc.if_nametoindex(name)
        self.addresses = {}

    def __str__(self):
        return " [%d] %s: IPv4=%s, IPv6=%s" % (
            self.index,
            self.name,
            self.addresses.get(AF_INET),
            self.addresses.get(AF_INET6),
            )

def get_network_interfaces():
    ifap = POINTER(struct_ifaddrs)()
    result = libc.getifaddrs(pointer(ifap))
    if result != 0:
        raise OSError(get_errno())
    del result
    try:
        retval = {}
        for ifa in ifap_iter(ifap):
            name = ifa.ifa_name
            i = retval.get(name)
            if not i:
                i = retval[name] = NetworkInterface(name)
            family, addr = getfamaddr(ifa.ifa_addr.contents)
            if addr:
                i.addresses[family] = addr
        return retval.values()
    finally:
        libc.freeifaddrs(ifap)

def choice_the_interface(nis, choice):
    for n in nis:
        if str(n.index) == choice:
            return n.name
    return None

if __name__ == '__main__':
    print("Vous démarez le script de configuration de MeshOui\n\n")
    nis = get_network_interfaces()
    for ni in nis:
        print(str(ni))
    goodchoice = False
    choice = raw_input("\nVeuillez choisir une interface de connection au mesh identifié par [x]: ")
    while not goodchoice:
        if choice in [str(n.index) for n in nis]:
            goodchoice = True
        else:
            choice = raw_input("Choix caca. Resaisissez une interface de connection identifié par [x]: ")
    inname = choice_the_interface(nis, choice)
    os.system("sudo ./start_bat.sh %s" % inname)
    ouinon = raw_input("\n\nVoulez vous ajouter un bridge? O/N :")
    if ouinon.lower() == 'o' or ouinon.lower() == 'oui':
        print("\n")
        for ni in nis:
            if not choice == str(ni.index):
                print(str(ni))
        goodchoice = False
        choice2 = raw_input("\nVeuillez choisir une interface de bridge identifié par [x]: ")
        while not goodchoice:
            if choice2 in [str(n.index) for n in nis] and not choice2 == choice:
                goodchoice = True
            else:
                choice2 = raw_input("Choix caca. Resaisissez une interface de bridge identifié par [x]: ")
        inname = choice_the_interface(nis, choice2)
        os.system("sudo ./start_bridge.sh %s" % inname)