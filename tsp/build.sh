#!/bin/bash

# https://stackoverflow.com/a/24112741
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

g++ -c -o tsp.o tsp.cpp
g++ -shared -o libtsp.so tsp.o
rm tsp.o
