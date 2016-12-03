#!/usr/bin/env python3

import sys
import os
import subprocess
from time import sleep

def kill_process():
    p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "cas"], stdin=p1.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p2.communicate()
    
    for line in out.split(os.linesep):
        if line.startswith('cc'):
            pid = line.split()[1]
            subprocess.run(['kill', '-9', pid])
            return

def stop_node():
    try:
        # Query local UUID
        output = subprocess.check_output(['/home/cc/cassandra/bin/nodetool', 'info'], universal_newlines=True)
        id = output.split(os.linesep)[0].split()[2]
        # kill process
        kill_process()
        # Wait for the info to be passed to seed
        sleep(15)
        # Use removenode on seed
        subprocess.run(['/home/cc/cassandra/bin/nodetool', '-h', '10.140.83.2', 'removenode', id])
    except subprocess.CalledProcessError as e:
        print(e.output)

def start_node():
    subprocess.run(['/home/cc/cassandra/bin/cassandra'])
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit()
    if sys.argv[1] == 'start':
        start_node()
    if sys.argv[1] == 'stop':
        stop_node()
