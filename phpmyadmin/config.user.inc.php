<?php
  $i++;
  $cfg['Servers'][$i]['verbose'] = 'backend';
  $cfg['Servers'][$i]['host'] = 'maria-db-hack';
  $cfg['Servers'][$i]['port'] = '';
  $cfg['Servers'][$i]['socket'] = '';
  $cfg['Servers'][$i]['connect_type'] = 'tcp';
  $cfg['Servers'][$i]['extension'] = 'mysqli';
  $cfg['Servers'][$i]['auth_type'] = 'config';
  $cfg['Servers'][$i]['user'] = 'root';
  $cfg['Servers'][$i]['password'] = 'password';
  $cfg['Servers'][$i]['AllowNoPassword'] = false;