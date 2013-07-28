#/bin/bash

set -x

fetch() {
  dir=${1}
  url=${2}
  if ! [ -d ${dir} ]; then
    curl -L -O ${url}
    mkdir ${dir}
    tar -xj -C ${dir} --strip-components 1 -f $(basename ${url})
  fi
}

EIGEN_URL=http://bitbucket.org/eigen/eigen/get/3.2.0.tar.bz2
fetch eigen $EIGEN_URL

GLOG_URL=https://google-glog.googlecode.com/files/glog-0.3.3.tar.gz
fetch glog $GLOG_URL

GFLAGS_URL=https://gflags.googlecode.com/files/gflags-2.0-no-svn-files.tar.gz
fetch gflags $GFLAGS_URL
