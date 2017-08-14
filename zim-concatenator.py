#!/usr/bin/env python

from os.path import expanduser
from os.path import exists
from os.path import isdir
from os.path import abspath
from os.path import join
from os.path import walk

from re import search
from re import compile

import subprocess

class Concatenator(object):
    def __init__(self, path, matching_regex_exp=r'(?P<prefix>\w+\.zim)(?P<suffix>\w+)'):
        self.path = path
        self.resolved_path = abspath(expanduser(self.path))
        if not exists(self.resolved_path) or not isdir(self.resolved_path):
            return
        self.matching_regex = compile(matching_regex_exp)
        self.groups_by_prefix = {}

    def group_by_prefix(self, arg, dirname, files):
        if len(files) <= 1:
            return

        for file in files:
            m = search(self.matching_regex, file)
            if m is None:
                continue

            m_dict = m.groupdict()
            prefix = m_dict['prefix']
            suffix = m_dict['suffix']
            new_file = join(dirname, prefix)
            already_there = self.groups_by_prefix.get(new_file)

            if already_there is None:
                already_there = []
                self.groups_by_prefix[new_file] = already_there

            already_there.append(join(dirname, prefix + suffix))

    def concatenate(self):
        for new_file, filenames in self.groups_by_prefix.items():
            filenames.sort()
            cmd = 'cat {}'.format(' '.join(filenames))
            exit_code = -1
            with open(new_file, 'wb') as f:
                f.write(subprocess.check_output([cmd], shell=True))

    def run(self):
        walk(self.resolved_path, self.group_by_prefix, '')
        self.concatenate()

if __name__ == '__main__':
    concatenator = Concatenator(path='.')
    concatenator.run()
