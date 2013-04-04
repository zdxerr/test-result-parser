# -*- coding: utf-8 -*-

import cPickle as pickle
from pprint import pprint

from result import ResultFile, Sequence


class CRTITAResultFile(ResultFile):
    def parse(self):
        with open(self.path, 'r') as result_file:
            self.__result = pickle.load(result_file)

        for key in self.__result:
            print key

        pprint(self.__result['EnvInfo'])

        # pprint(self.__result['TestResult'])


if __name__ == '__main__':
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\' \
                  'RTIFlexRay\\Res\\INT13\\T_01_RFT\\TS4\\Result\\' \
                  'crtita_result'
    result = CRTITAResultFile(result_path)
    print result
    # print result.time
    # print result.description

    # pprint(result.environment)
    # pprint(result.run)
    # pprint(result.sequences)
