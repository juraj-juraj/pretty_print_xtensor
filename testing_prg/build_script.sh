#!/bin/bash
# This script is used to build the testing program
mkdir build
cd build
# install the dependencies from conanfile.txt
conan install ..
# build the program, like a normal cmake project
cmake ..
make
