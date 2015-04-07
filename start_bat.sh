modprobe batman-adv

ifconfig $1 down

ifconfig $1 mtu 1528
iwconfig $1 mode ad-hoc essid meshoui ap 02:12:34:56:78:9A channel 1

batctl if add $1
ifconfig $1 up
ifconfig bat0 up