#!/bin/bash
#script delete all files and directory that we don't use after pulling from github repository

git pull
sudo rm -r docs/ example_* host/ _node_utils.sh project_cfg/ project_cfg/ project_* provision.sh README.md student_projects/ ucl_minimal_cfg/ ucl_topo Vagrantfile
