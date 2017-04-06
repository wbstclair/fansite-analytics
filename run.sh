#!/usr/bin/env bash

# Initiate log processing
python ./src/process_log.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/hours.txt ./log_output/resources.txt ./log_output/blocked.txt

# Local log
#python ./src/process_log.py ../Insight/log.txt ./log_output/hosts.txt ./log_output/hours.txt ./log_output/resources.txt ./log_output/blocked.txt