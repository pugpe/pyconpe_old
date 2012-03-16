from jinja2 import FileSystemLoader

from provy.more.debian import PipRole
from provy.more.debian import SupervisorRole as _SupervisorRole


class SupervisorRole(_SupervisorRole):
    '''Also change templates to make use of [include] section'''
    def register_fs_template_loader(self, path):
        if path not in self.context['registered_loaders']:
            self.context['loader'].loaders.append(FileSystemLoader(path))
            self.context['registered_loaders'].append(path)

    def provision(self):
        self.register_fs_template_loader('templates/')

        with self.using(PipRole) as role:
            role.ensure_package_installed('supervisor')
