#!/usr/bin/python3

import os, sys, syslog
from glob import glob
import argparse
import requests
import json
import subprocess
import shlex
from datetime import date
from datetime import datetime
import base64
import iiab.iiab_lib as iiab
import iiab.adm_lib as adm

# https://kolibri.readthedocs.io/en/latest/
# https://github.com/learningequality/kolibri/tree/develop/kolibri/core/content/management/commands

# RDC channels
c1 = '3ebfa70251cb4b69b33def14e37da05f'
c2 = '19edf228559c4e1ea231b4340603eff3'
c3 = '8ef0c1bf48a64049af202bd96c059cbf'

iiab_config_dir = "/etc/iiab"
# iiab_config_dir = "{{ iiab_config_dir }}"

kolibri_env = {}
kolibri_env['KOLIBRI_HOME'] = adm.CONST.kolibri_home
kolibri_user = adm.CONST.kolibri_user
kolibri_group =  adm.CONST.kolibri_group

def main ():
    try:
        args = parse_args()
    except:
        sys.exit(1)
    print(args)

    print ('Gettomg channel ', args.channel)
    cmd = '/usr/bin/kolibri manage importchannel -v 0 network '
    cmd_args = shlex.split(cmd + args.channel)
    p = subprocess.Popen(cmd_args, env=kolibri_env, group=kolibri_group, user=kolibri_user)
    p.wait()

    print ('Gettomg channel content ', args.channel)
    cmd = '/usr/bin/kolibri manage importcontent -v 0 network '
    cmd_args = shlex.split(cmd + args.channel)
    p = subprocess.Popen(cmd_args, env=kolibri_env, group=kolibri_group, user=kolibri_user)
    p.wait()


def parse_args():
    parser = argparse.ArgumentParser(description="Import Channel Content into Kolibri with option Node ID.")
    parser.add_argument("channel", help="The name of the channel.")
    parser.add_argument("--node", help="Only download starting at this Node ID. Call multiple time for different nodes", action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
   # Now run the main routine
    main()
