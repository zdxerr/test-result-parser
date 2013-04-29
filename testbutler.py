# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
from xml.parsers import expat
from pprint import pprint
import logging
import dateutil.parser

from result import ResultFile, Sequence


class TestbutlerParser(object):
    possible_states = {
        -1: None,
        0: "Ok",
        1: "Fail",
        2: "Crash",
        3: "Exception",
        4: "Blocked",
    }

    def parse(self):
        self.log = []

        self._parser = expat.ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data

        self._tags = []
        self.__entry_attrs = []
        self.__entries = []

        logging.debug("Parsing %r.", self.path)

        with open(self.path) as f:
            self._parser.ParseFile(f)

        del self._parser

        if self.path.lower().endswith('maintest.log.xml'):
            for path, folder, files in os.walk(os.path.dirname(self.path)):
                for filename in files:
                    if filename.lower().endswith('log.xml'):
                        if filename.lower() == 'maintest.log.xml':
                            continue
                        filepath = os.path.join(path, filename)
                        #name = os.path.relpath(filepath, os.path.dirname(self.path)).strip('.LOG.xml')
                        s = TestbutlerSequence(self, path=filepath)
                        #print name, filepath, os.path.dirname(self.path)

                        self.sequences.append(s)


    def start(self, tag, attrs):
        self._tags.append(tag)
        logging.debug("%s %r", "->".join(self._tags), attrs)

        # parse time attributes
        for k in ['time', 'changedate']:
            if k in attrs:
                attrs[k] = dateutil.parser.parse(attrs[k])

        if 'result' in attrs:
            self.state = self.possible_states.get(int(attrs['result']),
                                                  int(attrs['result']))

        if tag in ['logFile', 'testDesciption']:
            self.__dict__.update(attrs)
        elif tag == 'entry':
            self.__entry = {
                'state': self.possible_states.get(int(attrs['result'])),
                'time': attrs['time'],
                'log': []
            }

    def end(self, tag):
        assert(tag == self._tags.pop())
        if tag == 'entry':
            self.log.append(self.__entry)
            self.__entry = None

    def data(self, data):
        logging.debug("%s %r", "->".join(self._tags), data)
        if self._tags[-1] == 'log':
            self.__entry['log'].append(data.encode('utf-8'))


class TestbutlerResult(TestbutlerParser, ResultFile):
    """Parsing Testbutler result files."""
    pass


class TestbutlerSequence(TestbutlerParser, Sequence):
    def __init__(self, result, path=None):
        # id = os.path.relpath(path, os.path.dirname(result.path))[:-8]
        id = path[:len(os.path.dirname(result.path)) - 8]
        super(TestbutlerSequence, self).__init__(id)
        self.path = path
        self.parse()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\RTIxxxMM' \
                  '\\ResMT\\SCALEXIO PlugIns\\CANMM\\T_01\\MainTest.LOG.xml'
    result = TestbutlerResult(result_path)
    print result
    for s in result.sequences:
        print "*"*79
        print s
        for l in s.log[-10:]:
            print "#"*79
            print l['state'], l['time']
            print "".join(l['log'])
            # pprint(l)
