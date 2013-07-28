#!/bin/bash

THIS_DIR="$(dirname "${0}")"
cd ${THIS_DIR}
./download-prerequisites.sh

mkdir -p install

mkdir -p build/eigen
cd build/eigen
cmake ../../eigen -DCMAKE_INSTALL_PREFIX=${PWD}/../../install
make install
cd ../..

mkdir -p build/gflags
cd build/gflags
if ! [ -f config.status ]; then
  ../../gflags/configure --prefix=${PWD}/../../install
fi
make -j10
make install
cd ../..

mkdir -p build/glog
cd build/glog
if ! [ -f config.status ]; then
  ../../glog/configure --with-gflags=${PWD}/../../install \
                       --prefix=${PWD}/../../install
fi
make -j10
make install
cd ../..

mkdir -p build/protobuf
cd build/protobuf
if ! [ -f config.status ]; then
  ../../protobuf/configure --prefix=${PWD}/../../install
fi
make -j10
make install
cd ../..
