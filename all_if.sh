

ip link show | cut -d":" -f 2 | cut -d" " -f 2 | awk 'NR%2==1' | sed '/^lo$/d'
