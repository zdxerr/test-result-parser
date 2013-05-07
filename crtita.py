# -*- coding: utf-8 -*-

import cPickle as pickle
from pprint import pprint
from datetime import timedelta

import dateutil.parser

from result import ResultFile, Sequence


class CRTITAResult(ResultFile):
    def parse(self):
        with open(self.path, 'r') as result_file:
            self.__result = pickle.load(result_file)

        self.nodes.append('CRTITA')

        self.__parse_environment()
        self.__parse_run()
        self.__parse_sequences()

    def __parse_environment(self):
        env = self.__result['EnvInfo']

        self.os = env['6Operating system']
        self.pc = "N/A"
        self.platform = "N/A"

    def __parse_run(self):
        self.run = run = {}
        summary = self.__result['Summary']

        try:
            self.description = self.result['TestrunConfig']['TestDescription']
        except:
            pass

        self.start = dateutil.parser.parse(summary['Start time'], fuzzy=True)
        self.end = dateutil.parser.parse(summary['End time'], fuzzy=True)

    def __parse_sequences(self):
        self.sequences = sequences = []
        for name in sorted(self.__result['TestResult'].keys()):
            result = self.__result['TestResult'][name]
            s = CRTITASequence(name, result[0]['status'])
            sequences.append(s)
            s.comment = result[0]['comment']

            d = name.split('\\')
            s.name = d[-1]
            s.group = d[-2]
            s.nodes = d[:-2]

            # print '#'*8, result[0]['execTime']
            dt = dateutil.parser.parse(result[0]['execTime'], fuzzy=True)
            td = (timedelta(days=1)
                  if dt.time() < self.start.time()
                  else timedelta())

            d = (self.start + td).date()

            s.start = dt.replace(year=d.year, month=d.month, day=d.day)
            s.end = s.start + timedelta(
                seconds=float(result[0]['testDuration'].split(' ', 1)[0]))

            s.log = []
            for tc in result[0]['tcList']:
                s.log.append(
                    {
                        'id': tc['tcNum'],
                        'status': tc['status'],
                        'message': tc['tcName'].strip(),
                        'name': tc['tcName'].strip(),
                    }
                )
                if tc['userData']:
                    for ud in tc['userData']:
                        # for k, v in ud.items():
                        #     s.log.append(
                        #         {
                        #             'id': tc['tcNum'],
                        #             'status': tc['status'],
                        #             'message': "{} -> {}".format(k, v)
                        #         }
                        #     )
                        s.log[-1]['message'] += "\n" + "\n".join(
                            "{} -> {}".format(k, v) for k, v in ud.items())


class CRTITASequence(Sequence):
    possible_states = {
        0: "Ok",
        1: "Fail",
        2: "Fail",
        3: "Fail",
        4: "Fail",
        5: "Fail",
    }


if __name__ == '__main__':
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\' \
                  'RTIFlexRay\\Res\\INT13\\T_01_RFT\\TS4\\Result\\' \
                  'crtita_result'
    result = CRTITAResult(result_path)
    print result

    for sequence in result.sequences:
        # print sequence,
        print sequence.name, sequence.group, sequence.nodes
        # pprint(sequence.log)
    # print result.time
    # print result.description

    # pprint(result.environment)
    # pprint(result.run)
    # pprint(result.sequences)
