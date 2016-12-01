#!/usr/bin/env python3

import sys
import subprocess
import json

def config_network(network, targets, mapping):
    num_targets = len(targets)
    num_bands = num_targets + 1
    subprocess.run(['tc', 'qdisc', 'del', 'dev', network, 'root'])
    subprocess.run(['tc', 'qdisc', 'add', 'dev', network, 'root', 'handle', '1:', 'prio', 'bands', str(num_bands)])
    
    counter = 1
    handle_counter = 2
    for t in targets:
        ip = mapping[t['target']]
        lat = t['latency']
        subprocess.run(['tc', 'qdisc', 'add', 'dev', network, 'parent', '1:{}'.format(counter),
                        'handle', '{}:'.format(handle_counter), 'netem', 'delay', '{}ms'.format(lat)])
        subprocess.run(['tc', 'filter', 'add', 'dev', network, 'parent', '1:0', 'protocol', 'ip', 'prio', '1',
                        'u32', 'match', 'ip', 'dst', ip, 'flowid', '{}:1'.format(handle_counter)])
        counter += 1
        handle_counter += 1

def unconfig_network(network):
    subprocess.run(['tc', 'qdisc', 'del', 'dev', network, 'root'])

def print_help():
    print("Usage:\t network_latency add local_ip network_interface")
    print("\t network_latency remove network_interface")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print_help()
        exit()
    if sys.argv[1] == 'add':       
        with open('network_latency.json') as json_data:
            json = json.load(json_data)
            local_ip = sys.argv[2]
            network = sys.argv[3]
            for i in json['topology']:
                if i['local'] == local_ip:
                    config_network(network, i['targets'], json['mapping'])
                    exit()
            print('the given ip not found in config file')
    elif sys.argv[1] == 'remove':
        unconfig_network(sys.argv[2])
    else:   
        print_help()
        exit()
    
