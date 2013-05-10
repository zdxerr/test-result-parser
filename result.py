# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime

TAG_EXPRESSIONS = [
    re.compile(r'ImplSW_RLS_[0-9]+-[AB]'),
    re.compile(r'INT[0-9]+'),
    re.compile(r'PPF[0-9]+'),
    re.compile(r'RC[0-9_]+'),
    re.compile(r'T_[0-9]+'),
]

NODE_EXPRESSIONS = [
    re.compile(r'RTI(xxxMM|FlexRay)'),
]


class ResultFile(object):
    """Base class for all result file parsers."""

    def __init__(self, path):
        if not os.path.isfile(path):
            raise IOError("File not found: {}".format(path))
        self.path = path
        self.created = datetime.fromtimestamp(os.stat(self.path).st_ctime)

        self.nodes = [t for t in path.split(os.path.sep)
                      if any(r.match(t) for r in NODE_EXPRESSIONS)]

        self.label = "_".join(
            t for t in path.split(os.path.sep)
            if any(r.match(t) for r in TAG_EXPRESSIONS))

        self.description = ""
        self.sequences = []

        self.parse()

    def __repr__(self):
        return "<ResultFile at {!r}>".format(self.path)

    def parse(self):
        raise NotImplementedError(self.parse)


class Sequence(object):
    """Base class for all sequence results."""
    possible_states = {}

    def __init__(self, id, state=None):
        self.id = id
        self.state = self.possible_states.get(state, state)
        self.comment = ""
        self.log = []

    def __repr__(self):
        return "<Sequence {!r}: {}>".format(self.id, self.state)

if __name__ == '__main__':
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\' \
                  'RTIxxxMM\\Res\\INT17\\T_01\\ts_results_rti1005.mat'
    try:
        result = ResultFile(result_path)
    except NotImplementedError:
        pass
    else:
        print result
