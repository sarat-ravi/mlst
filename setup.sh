# #!/bin/bash
# This script sets shell environment variables and creates a go directory
# First install go:
#   sudo apt-get install golang-go #Unix
#   homebrew install go #MacOSX
# Then source this file by running source setup.sh

which go &>/dev/null
if [ $? -eq 1 ]; then
  echo Please install go first
  exit 1
fi

eval `go env` #set global environment variables for go
echo setting go global variables

export GOPATH=${HOME}/.go
export GOBIN=${GOROOT}/bin/
export PATH=${PATH}:${GOBIN}

function setupgo(){
  if [ ! -d ${HOME}/.go ]; then
    #https://piazza.com/class#spring2013/cs170/649
    echo installing dependencies to $GOPATH
    local DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" #http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
    mkdir ${HOME}/.go
    mkdir -p $GOPATH/src
    cp -r $DIR $GOPATH/src
    cd $DIR/..

     #install checker programs
    go install mlst/check_input mlst/check_output

    #remove git repo from go dependencies
    if [ -d ${HOME}/.go/.git ]; then
      rm -rf ${HOME}/.go/.git
    fi
    cd $OLDPWD
  else
    echo already installed dependencies to $GOPATH
    echo To reinstall rm -rf $GOPATH and source this file again
  fi
}

setupgo


