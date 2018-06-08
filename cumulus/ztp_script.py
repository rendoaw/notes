#!/usr/bin/env python
# CUMULUS-AUTOPROVISIONING

from subprocess import Popen, PIPE, STDOUT
import os
import sys
import syslog
import logging
from logging.handlers import SysLogHandler

CUMULUS_LOGFILE = "/var/log/ztp.log"




def cumulus_ztp():

    if os.path.exists(CUMULUS_LOGFILE):
        os.remove(CUMULUS_LOGFILE)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(CUMULUS_LOGFILE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(fh)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logging.getLogger().addHandler(consoleHandler)

    def run_shell_command(cmd):
        logger.info("[cmd->] "+cmd)
        response = ""
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in p.stdout.readlines():
            #logging.info("[<-output] "+line)
            response = response + str(line)
            #originally p.wait(10), python 2.7 requires no argument
            p.wait()
        logging.info("[<-shell response] "+response)
        rc = p.returncode
        return rc

    def install_license():
        license = ""
        logging.info("Installing license")
        ret = run_shell_command("echo "+license+" | /usr/cumulus/bin/cl-license -i")
        if rt != 0:
            logging.error("ERROR: License not installed. Return code was: "+str(rc))

    def wait_for_nclu():
        while True:
            cmd = "net show interface"
            ret = run_shell_command(cmd)
            if ret == 0:
                break

    def init_ztp():
        logging.info("add debian repository")
        cmd = "echo \"deb http://http.us.debian.org/debian jessie main\" >> /etc/apt/sources.list"
        run_shell_command(cmd)
        cmd = "echo \"deb http://security.debian.org/ jessie/updates main\" >> /etc/apt/sources.list"
        run_shell_command(cmd)
        cmd = "apt-get update -y && apt-get install -y netshow htop vim"
        run_shell_command(cmd)

        #install_license()

        cmd = "ifreload -a"
        run_shell_command(cmd)

        wait_for_nclu()

        #cmd = "net add vrf mgmt"
        #run_shell_command(cmd)
        cmd = "net add time zone Etc/UTC"
        run_shell_command(cmd)
        cmd = "net add time ntp server 192.168.0.254 iburst"
        run_shell_command(cmd)
        cmd = "net commit"
        run_shell_command(cmd)

        #cmd = ""
        #run_shell_command(cmd)

    init_ztp()



if __name__ == "__main__":
    cumulus_ztp()
    sys.exit(0)
