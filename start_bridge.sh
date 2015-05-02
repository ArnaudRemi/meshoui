#!/usr/bin/env bash
ifconfig bat0 down

brctl addbr mesh-bridge
brctl addif mesh-bridge $1
brctl addif mesh-bridge bat0

ifconfig $1 up
ifconfig bat0 up
ifconfig mesh-bridge up