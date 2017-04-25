class eggsnspam {

  package { ['sqlite3']:
    ensure => present;
  }

  file { '/home/vagrant/eggsnspam':
    ensure => 'link',
    target => '/vagrant',
  }

  file { '/home/vagrant/.virtualenvs':
    ensure => 'directory',
  }

  exec { 'init_database':
    command     => '/home/vagrant/eggsnspam/bin/init_db.sh',
    creates     => '/home/vagrant/eggsnspam/eggsnspam.db',
    cwd         => '/home/vagrant/eggsnspam',
    require     => File['/home/vagrant/eggsnspam'],
  }

  class { 'python' :
    version    => 'system',
    pip        => 'present',
    dev        => 'present',
    virtualenv => 'present',
    gunicorn   => 'absent',
  }

  python::virtualenv { '/home/vagrant/eggsnspam' :
    ensure       => present,
    version      => 'system',
    requirements => '/vagrant/requirements.txt',
    systempkgs   => false,
    distribute   => false,
    venv_dir     => '/home/vagrant/.virtualenvs/eggsnspam',
    owner        => 'vagrant',
    group        => 'vagrant',
    cwd          => '/home/vagrant/eggsnspam',
    require      => [ File['/home/vagrant/.virtualenvs'], File['/home/vagrant/eggsnspam'], Class['python'] ]
  }
}
