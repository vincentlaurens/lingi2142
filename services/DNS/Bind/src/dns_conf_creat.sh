#!/bin/bash

PATH_SRC='/home/vagrant/lingi2142/end_user_management/bind/src'

sudo python3 $PATH_SRC/dns_write_files.py

sudo python3 $PATH_SRC/dns_write_db_files.py