# -*- coding: utf-8 -*-

import os
from xml.parsers import expat
from pprint import pprint
import logging
import dateutil.parser

from result import ResultFile, Sequence

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                    datefmt='"%Y-%m-%d %H:%M:%S"', level=logging.DEBUG)

class TestbutlerParser(object):
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

        # parse entries
        for path, name in self.__entries:
            sequence_path = os.path.join(os.path.dirname(self.path), path)
            print sequence_path,
            # for f in os.listdir(sequence_path):

            print [ for f in os.listdir(sequence_path) if name in f]


    def start(self, tag, attrs):
        self._tags.append(tag)
        print "->".join(self._tags), attrs

        # parse time attributes
        if 'time' in attrs:
            attrs['time'] = dateutil.parser.parse(attrs['time'])

        if tag in ['logFile', 'testDesciption']:
            self.__dict__.update(attrs)
        elif tag == 'entry':
            attrs['log'] = []
            self.__entry_attrs.append(attrs)
        elif tag == 'log':
            self.log = True

        # elif tag == 'result':
        #     print attrs
        #     self.result.update(attrs)

    def end(self, tag):
        assert(tag == self._tags.pop())
        if tag == 'log':
            self.log = {}

    def data(self, data):
        print "->".join(self._tags), repr(data)
        if self.log:
            if data.startswith("[xml]"):
                self.__entries.append(data[6:].rsplit(" - ", 1))
        else:
            pass


class TestbutlerResult(TestbutlerParser, ResultFile):
    """Parsing Testbutler result files."""
    pass


class TestbutlerSequence(TestbutlerParser, Sequence):
    possible_states = {
        -1: "Not Executed",
        0: "Ok",
        1: "Fail",
        2: "Crash",
        3: "Exception",
        4: "Blocked",
    }

    def __init__(self, name, state=None, path=None):
        super(TestbutlerSequence, self).__init__(name, state)
        self.path = path
        self.parse()


if __name__ == '__main__':
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\RTIxxxMM' \
                  '\\ResMT\\SCALEXIO PlugIns\\CANMM\\T_01\\MainTest.LOG.xml'
    result = TestbutlerResult(result_path)
    print result
    #pprint(result.sequences)
