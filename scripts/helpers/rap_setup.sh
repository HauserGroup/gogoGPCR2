#!/bin/bash

# This script sets up the environment on the RAP platform

MY_SSH=$1
GIT_EMAIL=$2
GIT_USER=$3

# Download SSH keys from a remote location specified by $MY_SSH, usually /.ssh
dx download -r $MY_SSH

# Set the correct permissions for the SSH private key
chmod 400 .ssh/id_ed25519

# Start the SSH agent and add the private key to it
eval "$(ssh-agent -s)"
ssh-add .ssh/id_ed25519

# The rest
git config --global user.email $GIT_EMAIL
git config --global user.name $GIT_USER
git clone git@github.com:HauserGroup/gogoGPCR2.git
cd gogoGPCR2/
pip install -e .
