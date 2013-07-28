#/bin/bash

set -x

EIGEN_URL=http://bitbucket.org/eigen/eigen/get/3.2.0.tar.bz2
if ! [ -d eigen ]; then
  curl -L -O ${EIGEN_URL}
  mkdir eigen
  tar -xj -C eigen --strip-components 1 -f $(basename ${EIGEN_URL})
fi

GLOG_URL=https://google-glog.googlecode.com/files/glog-0.3.3.tar.gz
if ! [ -d glog ]; then
  curl -L -O ${GLOG_URL}
  mkdir glog
  tar -xj -C glog --strip-components 1 -f $(basename ${GLOG_URL})
fi

GFLAGS_URL=https://gflags.googlecode.com/files/gflags-2.0-no-svn-files.tar.gz
if ! [ -d gflags ]; then
  curl -L -O ${GFLAGS_URL}
  mkdir gflags
  tar -xj -C gflags --strip-components 1 -f $(basename ${GFLAGS_URL})
fi
