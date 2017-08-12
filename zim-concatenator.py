#!/usr/bin/env python

from os.path import expanduser
from os.path import exists
from os.path import isdir
from os.path import abspath
from os.path import join

from re import search
from re import compile

class Concatenator(object):
    def __init__(self, path, matching_regex_exp=r'(?P<prefix>\w+\.zim)(?P<suffix>\w+)'):
        if not exists(path) or not isdir(path):
            return
        self.matching_regex = compile(matching_regex_exp)
        self.path = path
        self.resolved_path = abspath(expanduser(self.path))

    def concatenate(self, arg, dirname, files):
        def is_match(name):
            return search(self.matching_regex, name)
        matches = filter(is_match, files)

    def run(self):
        walk(self.resolve_path, self.concatenate, '')

if __name__ == '__name__':
    concatenator = Concatenator('.')
    concatenator.run()
