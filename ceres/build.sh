#!/bin/bash

THIS_DIR="$(dirname "${0}")"
${THIS_DIR}/download-prerequisites.sh

mkdir -p install

mkdir -p build
cd build
../gflags/configure --prefix=$PWD/../install
make -j10
make install
