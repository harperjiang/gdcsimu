#!/bin/bash

ssh -t cc@cas-a 'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py add a eno1'
ssh -t cc@cas-b  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py add b eno1'
ssh -t cc@cas-c  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py add c eno1'
ssh -t cc@cas-d  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py add d eno1'
ssh -t cc@cas-e  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py add e eno1'
ssh -t cc@cas-f 'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py add f eno1'
