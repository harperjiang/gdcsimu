#!/usr/bin/env python3

import sys
import subprocess
import json

def config_network(network, targets, mapping, params):
    num_targets = len(targets)
    num_bands = num_targets + 1
    
    lat_ratio = params['latency_ratio']
    
    subprocess.run(['tc', 'qdisc', 'del', 'dev', network, 'root'])
    subprocess.run(['tc', 'qdisc', 'add', 'dev', network, 'root', 'handle', '1:', 'prio', 'bands', str(num_bands)])
    
    handle_counter = 1
    for t in targets:
        ip = mapping[t['target']]
        lat = int(t['latency'] * lat_ratio)
        subprocess.run(['tc', 'qdisc', 'add', 'dev', network, 'parent', '1:{}'.format(handle_counter + 1),
                        'handle', '{}:'.format(handle_counter + 1), 'netem', 'delay', '{}ms'.format(lat)])
        subprocess.run(['tc', 'filter', 'add', 'dev', network, 'protocol', 'ip', 'parent', '1:', 'prio', '1',
                        'u32', 'match', 'ip', 'dst', ip, 'flowid', '1:{}'.format(handle_counter)])
        handle_counter += 1
    # Direct all remaining traffic
    subprocess.run(['tc', 'filter', 'add' , 'dev', network,
                    'protocol', 'ip', 'parent', '1:' , 'prio', '2',
                    'u32', 'match', 'ip' , 'src', '0.0.0.0/0', 'flowid', '1:1'])

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
                    config_network(network, i['targets'], json['mapping'], json['params'])
                    exit()
            print('the given ip not found in config file')
    elif sys.argv[1] == 'remove':
        unconfig_network(sys.argv[2])
    else:   
        print_help()
        exit()
    
