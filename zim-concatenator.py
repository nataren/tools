#!/usr/bin/env python

from os.path import expanduser
from os.path import exists
from os.path import isdir
from os.path import abspath
from os.path import join
from os.path import walk

from re import search
from re import compile

class Concatenator(object):
    @property
    def dict(self):
        return self.groups_by_prefix

    def __init__(self, path, matching_regex_exp=r'(?P<prefix>\w+\.zim)(?P<suffix>\w+)'):
        self.path = path
        self.resolved_path = abspath(expanduser(self.path))
        if not exists(self.resolved_path) or not isdir(self.resolved_path):
            return
        self.matching_regex = compile(matching_regex_exp)
        self.groups_by_prefix = {}

    def concatenate(self, arg, dirname, files):
        def is_match(name):
            return search(self.matching_regex, name)

        for file in files:
            m = search(self.matching_regex, file)
            if m is not None:
                m_dict = m.groupdict()
                prefix = m_dict['prefix']
                suffix = m_dict['suffix']
                already_there = self.groups_by_prefix.get(prefix)
                if already_there is None:
                    already_there = []
                    self.groups_by_prefix[prefix] = already_there
                already_there.append(prefix + suffix)

    def run(self):
        walk(self.resolved_path, self.concatenate, '')

if __name__ == '__main__':
    concatenator = Concatenator(path='.')
    concatenator.run()
    print(concatenator.dict)
