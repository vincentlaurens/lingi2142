#!/usr/bin/env python3

import json
import os
import stat

from constants import PATH, PREFIXES_ADDRESS

with open(PATH + 'host_configuration.json') as data_file:
    data = json.load(data_file)

for host, configs in data.items():
    host_start_config = open(PATH + "group3_cfg/" + host + "_start.sh", "w")
    host_start_config.write("#!/bin/bash \n\n")
    host_start_config.write(
        "# This file has been generated automatically, see service_config_creation.py for details. \n\n")

    # Interface to LAN
    interface = host + "-eth0"
    for prefix_address in PREFIXES_ADDRESS:
        host_start_config.write(
            "ip address add dev " + interface + " " + prefix_address + configs["City"] + configs["site"] + configs[
                "use"] + configs["machine_number"] + "/64\n")
        host_start_config.write("\n")
    # Add the default route and route to providers
    host_start_config.write(
            "ip -6 route add ::/0 via " + PREFIXES_ADDRESS[0] + configs["City"] + configs["site"] + configs[
                "use"] + "::" + configs["prefix_default_route"] + " \n")
    host_start_config.write(
            "ip -6 route add " + PREFIXES_ADDRESS[1] + configs["City"] + configs["site"] + configs["use"] + "::" +
            configs["prefix_default_route"] + " dev " + host + "-eth0 \n\n")

    if "bind9" in configs:
        host_start_config.write("named -6 -c /etc/bind/" + configs["bind9"] + ".conf \n\n")

 #   if "extra_commands" in configs:
  #      for command in configs["extra_commands"]:
   #         host_start_config.write(command + "\n\n")

    host_start_config.close()
    # Add execution right to new file
    file_stat = os.stat(PATH + "group3_cfg/" + host + "_start.sh")
    os.chmod(PATH + "group3_cfg/" + host + "_start.sh", file_stat.st_mode | stat.S_IEXEC)
