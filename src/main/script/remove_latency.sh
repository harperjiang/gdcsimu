#!/bin/bash

ssh -i ~/chameleon_uc.pem -t cc@10.140.83.2  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py remove eno1'
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.6  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py remove eno1'
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.5  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py remove eno1'
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.7  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py remove eno1'
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.8  'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py remove eno1'
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.81 'cd ~/gdcsimu/src/main/script/; sudo ./network_latency.py remove eno1'
