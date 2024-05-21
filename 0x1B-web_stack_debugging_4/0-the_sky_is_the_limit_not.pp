# Fix stack so that we get to 0 failed requests

exec { 'sed':
  command => "sed -i 's/worker_connections .*/worker_connections 1024;/' /etc/nginx/nginx.conf",
  path    => ['/bin', '/usr/bin'],
}

exec { 'restart':
  command     => 'systemctl restart nginx',
  path        => ['/bin', '/usr/bin'],
  subscribe   => Exec['sed'],
}
