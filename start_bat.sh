modprobe batman-adv

ifconfig $1 down

ifconfig $1 mtu 1528
iwconfig $1 mode ad-hoc essid meshoui ap 6d:65:73:68:6f:75 channel 1

batctl if add $1
ifconfig $1 up
ifconfig bat0 up