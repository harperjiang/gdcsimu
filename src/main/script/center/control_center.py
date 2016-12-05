#!/usr/bin/env python3
import json
import time
import sys
import os
import logging
import subprocess

interval = 1  # 120s

def setup_logger():
    logging.basicConfig(level=logging.INFO)
    rootlogger = logging.root
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    rootlogger.addHandler(ch)

def start_remote(node):
    logger = logging.getLogger("CC")
    logger.info("Starting node {}".format(node))
    # subprocess.run(['ssh', node, '"python3 gdcsimu/src/main/script/node_control.py start"'])
    pass

def stop_remote(node):
    logger = logging.getLogger("CC")
    logger.info("Stopping node {}".format(node))
    # subprocess.run(['ssh', node, '"python3 gdcsimu/src/main/script/node_control.py stop"'])
    
    
def load_config():
    with open('control_trace.json') as json_data:
        jsobj = json.load(json_data)
        mappings = jsobj['mappings']
        traces = jsobj['traces']
        
        traceMap = {}
        
        for trace in traces:
            traceMap[trace['id']] = trace['trace']
        
        for mapping in mappings:
            mapping['trace'] = traceMap[mapping['id']]
            mapping['state'] = 1
        return mappings
    
def cc_start():
    logger = logging.getLogger("CC")
    logger.info('Starting Control Center')
    config = load_config()
    
    counter = 0
    while True:
        for item in config:
            trace = item['trace']
            if len(trace) <= counter:
                logger.info("Trace complete after {} loops. Exit".format(counter))
                exit()
            node = item['node']
            current_state = item['state']
            next_state = int(trace[counter])
            if current_state != next_state:
                if(next_state == 0):
                    stop_remote(node)
                if(next_state == 1):
                    start_remote(node)
            item['state'] = next_state
            counter += 1
            time.sleep(interval)    

def cc_stop(): 
    logger = logging.getLogger("CC")
    logger.info('Stopping Control Center') 
    p1 = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "control_center.py"],
                          stdin=p1.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    out, err = p2.communicate()
    
    for line in out.split(os.linesep):
        if line.startswith('cc') and ('grep' not in line):
            logger.info('Found Control Center Process, killing it')
            pid = line.split()[1]
            subprocess.run(['kill', '-9', pid])
            return
    logger.info("No running Control Center found, exiting")
    return

def print_help():
    print("Usage : control_center.py start/stop")    

if __name__ == "__main__":
    setup_logger()
    if len(sys.argv) == 1:
        print_help()
        exit()
    if sys.argv[1] == 'start':
        cc_start()
    elif sys.argv[1] == 'stop':
        cc_stop()
