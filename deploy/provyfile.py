#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from os.path import join

from fabric.api import put

from provy.core import Role, AskFor
from provy.more.debian import AptitudeRole, UserRole, PipRole, NginxRole
from provy.more.debian import GitRole, MySQLRole, MemcachedRole

from supervisor import SupervisorRole


class PreSetupRole(Role):
    def provision(self):
        new_user = self.context['new_user']

        self.execute('apt-get update', stdout=False, sudo=False)
        self.execute('apt-get install -y sudo', stdout=False, sudo=False)
        self.execute('apt-get install -y python', stdout=False, sudo=False)

        with self.using(UserRole) as role:
            role.ensure_group('admin')
            self.ensure_line('%admin  ALL=(ALL) NOPASSWD: ALL', '/etc/sudoers',
                             sudo=True)
            role.ensure_user(new_user, is_admin=True)

        # TODO: Melhorar
        self.ensure_dir('/home/{0}/.ssh/'.format(new_user), owner=new_user)
        self.change_dir_mode('/home/{0}/.ssh/'.format(new_user), 700)

        authorized_keys = '/home/{0}/.ssh/authorized_keys'.format(new_user)

        file = join(os.path.dirname(os.path.abspath(__file__)), 'files/id_rsa.pub')
        put(file, '/home/{0}/.ssh/'.format(new_user))
        cmd = 'cat /home/{0}/.ssh/id_rsa.pub >> {1}'.format(new_user, authorized_keys)
        self.execute(cmd, sudo=True)

        self.change_file_owner(authorized_keys, new_user)
        self.change_file_mode(authorized_keys, 600)
        # TODO: Disable root login


class MainServer(Role):
    def provision(self):
        self.log('Starting MySQLRole')
        with self.using(MySQLRole) as role:
            role.ensure_user(
                username=self.context['mysql_user'], login_from="%",
                identified_by=self.context['mysql_password'],
            )
            role.ensure_database(self.context['mysql_database'])
            role.ensure_grant(
                'ALL PRIVILEGES', on=self.context['mysql_database'],
                username=self.context['mysql_user'], login_from='%',
            )

        self.log('Starting NginxRole')
        with self.using(NginxRole) as role:
            role.ensure_conf(conf_template='nginx.conf')
            role.ensure_site_disabled('default')

            role.create_site(
                site=self.context['site'],
                template=self.context['template'],
            )
            role.ensure_site_enabled(self.context['site'])

        self.log('Starting MemcachedRole')
        self.provision_role(MemcachedRole)

        self.log('Starting SupervisorRole')
        with self.using(SupervisorRole) as role:
            self.ensure_dir('/var/log/supervisor', sudo=True)
            self.ensure_dir(self.context['include_dir'], sudo=True)

            role.config(
                config_file_directory='/etc/',
                log_folder='/var/log/supervisor',
                user='root',
            )
            include = self.context['include']
            # Should config have kwargs?
            role.context['supervisor-config']['include'] = include
            role.restart()

        self.log('Starting GitRole')
        with self.using(GitRole) as role:
            role.ensure_repository(
                self.context['repo'], self.context['project_path'],
                self.context['owner'],
            )
        # settings_local
        settings_file = 'settings_local.py'
        self.update_file(
            settings_file,
            join(self.context['project_path'], settings_file),
            options=self.context,
        )

        self.log('Starting Virtualenv')
        with self.using(PipRole) as role:
            role.ensure_package_installed('virtualenv')

        self.log('Starting deps')
        with self.using(AptitudeRole) as role:
            # Deps for PIL
            role.ensure_package_installed('zlib-devel')
            role.ensure_package_installed('libjpeg-devel')
            role.ensure_package_installed('freetype-devel')

            # Deps for Mysql (driver)
            role.ensure_package_installed('mysql-devel')


#address = 'pugpe.nodegrid.com'
address = '23.21.106.248'

servers = {
    'pre_setup': {
        'address': address,
        'user': 'root',
        'roles': [
            PreSetupRole,
        ],
        'options': {
            'new_user': 'pugpe',
        }
    },

    'frontend': {
        'address': address,
        'user': 'pugpe',
        'roles': [
            MainServer
        ],
        'options': {
            # mysql
            'mysql_user': 'pugpe',
            'mysql_password': AskFor('mysql_password', 'Mysql password'),
            'mysql_database': 'pug',

            # supervisord
            'include_dir': '/etc/supervisor/conf.d/',
            'include': '/etc/supervisor/conf.d/*.conf',

            # Project specific
            'site': 'pugpe',
            'template': 'pugpe',

            'repo': 'git://github.com/pugpe/pyconpe.git',
            'project_path': '/srv/pyconpe/',
        },
    },
}
