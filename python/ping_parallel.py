#!/usr/bin/env python

import threading
import subprocess
import os
import sys


MAX_PROCESSES = 25
semaphore = threading.Semaphore(MAX_PROCESSES)


def read_file(filename):
    cmds = ""
    lines = []
    if str(filename) is not '' and not os.stat(filename).st_size == 0:
        try:
            finput = open(filename, 'r')
            lines = [x.replace('\n', '') for x in finput]
            finput.close()
        except:
            return lines
    return lines


def ping_thread(hostname):
    with semaphore:
        cmd = "ping -c 2 "+hostname
        response = ""
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in p.stdout.readlines():
            response = response + str(line)
            p.wait()
        if p.returncode == 0:
            print hostname+" is UP"
            FO.write(hostname+" is UP\n")
        else:
            print hostname+" is DOWN"
            FO.write(hostname+" is DOWN\n")
        return



if __name__ == "__main__":
    target = read_file(sys.argv[1])
    FO = open(sys.argv[2],'w')

    for hostname in target:
        hostname = hostname.strip()
        threading.Thread(target=ping_thread, args=(hostname,)).start()
