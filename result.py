# -*- coding: utf-8 -*-

import os
from datetime import datetime

COMMON_RESULT_PATH = r'R:\PE\Testdata\CRTI-Test'


class ResultFile(object):
    """Base class for all result file parsers."""

    def __init__(self, path):
        self.path = path
        self.created = datetime.fromtimestamp(os.stat(self.path).st_ctime)

        # derive tags from path
        # relpath = os.path.relpath(self.path, COMMON_RESULT_PATH)
        relpath = self.path[len(COMMON_RESULT_PATH):]  # workaround
        self.tags = relpath.strip(os.path.sep).split(os.path.sep)
        self.description = ""
        self.time = None
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
