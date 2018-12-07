#!/bin/bash

PATH_SRC='/vagrant/services/DNS/bind2/src'


sudo python3 $PATH_SRC/dns_writes_files.py

sudo python3 $PATH_SRC/dns_write_db_files.py