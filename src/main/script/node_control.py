#!/usr/bin/env python3

import subprocess

def kill_process():
    p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "cas"], stdin=p1.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p2.communicate()
    
    for line in out.split(os.linesep):
        if line.startsWith('cc'):
            pid = line.split('\s+')[1]
            subprocess.run(['kill', '-9', pid])
            exit()

def stop_node():
    # Use decommission
    subprocess.run(['~/cassandra/bin/nodetool'])

def start_node():
    subprocess.run(['~/cassandra/bin/cassandra'])