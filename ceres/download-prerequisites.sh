#/bin/bash

set -x

EIGEN_URL=http://bitbucket.org/eigen/eigen/get/3.2.0.tar.bz2
if ! [ -d eigen ]; then
  curl -L -O ${EIGEN_URL}
  mkdir eigen
  tar -xj -C eigen --strip-components 1 -f $(basename ${EIGEN_URL})
fi
