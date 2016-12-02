#!/bin/bash

ssh -i ~/chameleon_uc.pem -t cc@10.140.83.2  "$1"
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.6  "$1"
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.5  "$1"
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.7  "$1"
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.8  "$1"
ssh -i ~/chameleon_uc.pem -t cc@10.140.83.81 "$1"
