# create a new run stage to ensure certain modules are included first
stage { 'pre':
  before => Stage['main']
}

# add the modules to the new 'pre' run stage
class { 'baseconfig':
  stage => 'pre'
}

# set defaults for file ownership/permissions
File {
  owner => 'vagrant',
  group => 'vagrant',
  mode  => '0644',
}

include baseconfig
include eggsnspam
