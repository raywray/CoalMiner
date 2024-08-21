#!/bin/bash

rm -rf output/

cp example_input_files/hops_* .

python3 coalminer.py /home/raya/Documents/Projects/CoalMiner/example_input_files/user_input_hops_k4.yml

rm -rf hops_*