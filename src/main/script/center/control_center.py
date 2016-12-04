#!/usr/bin/env python3
import json
import time
import subprocess

interval = 1  # 120s

def start_remote(node):
    print("Starting node {}".format(node))
    pass

def stop_remote(node):
    print("Stopping node {}".format(node))
    subprocess.run(['ssh',node,'-t','"python3 gdcsimu/src/main/script/node_control.py stop"'])
    
    
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
    
if __name__ == "__main__":
    config = load_config()
    print(config)
    
    counter = 0
    while True:
        for item in config:
            trace = item['trace']
            if len(trace) <= counter:
                print("Trace complete after {} loops. Exit".format(counter))
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
            
