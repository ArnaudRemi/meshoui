# Use those functions to enumerate all interfaces available on the system using Python.
# found on <http://code.activestate.com/recipes/439093/#c1>
"""
import socket
import fcntl
import struct
import array

def all_interfaces():
    max_possible = 128  # arbitrary. raise if needed.
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * bytes)

    # --- Debug
    print('byte : {}  -- buffer_info : {}'.format(bytes, names.buffer_info()[0]))
    # packed = struct.pack('iL', bytes, names.buffer_info()[0])
    # print(packed)
    # print(struct.unpack('iL', packed))

    print(s.fileno()) # fileno = filedescriptor of the socket.

    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]

    print(outbytes)

    namestr = names.tostring()

    print(namestr)

    lst = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split(b'\0', 1)[0]
        ip   = namestr[i+20:i+24]
        print(ip)
        lst.append((name, ip))

    print(lst)
    return lst

def format_ip(addr):
    # return str(ord(addr[0])) + '.' + \
    #        str(ord(addr[1])) + '.' + \
    #        str(ord(addr[2])) + '.' + \
    #        str(ord(addr[3]))
    return '{}.{}.{}.{}'.format(addr[0], addr[1], addr[2], addr[3])


ifs = all_interfaces()
for i in ifs:
    print("%12s   %s" % (i[0], format_ip(i[1])))
"""

import fcntl
import array
import struct
import socket
import platform

# global constants.  If you don't like 'em here,
# move 'em inside the function definition.
SIOCGIFCONF = 0x8912
MAXBYTES = 8096

def localifs():
    """
    Used to get a list of the up interfaces and associated IP addresses
    on this machine (linux only).

    Returns:
        List of interface tuples.  Each tuple consists of
        (interface name, interface IP)
    """
    global SIOCGIFCONF
    global MAXBYTES

    arch = platform.architecture()[0]

    # I really don't know what to call these right now
    var1 = -1
    var2 = -1
    if arch == '32bit':
        var1 = 32
        var2 = 32
    elif arch == '64bit':
        var1 = 16
        var2 = 40
    else:
        raise OSError("Unknown architecture: %s" % arch)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * MAXBYTES)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        sock.fileno(),
        SIOCGIFCONF,
        struct.pack('iL', MAXBYTES, names.buffer_info()[0])
        ))[0]

    namestr = names.tostring()
    return [(namestr[i:i+var1].split(b'\0', 1)[0], socket.inet_ntoa(namestr[i+20:i+24])) \
            for i in range(0, outbytes, var2)]

print(localifs())
