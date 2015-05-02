#!/usr/bin/env bash

brctl delif mesh-bridge bat0
brctl delif mesh-bridge $2
brctl delbr mesh-bridge

batctl if del $1

