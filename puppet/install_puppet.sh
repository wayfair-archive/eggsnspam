#!/bin/bash

(which puppet) || apt-get install -y puppet
mkdir -p /etc/puppet/modules
(puppet module list |grep stankevich-python ) || puppet module install stankevich-python