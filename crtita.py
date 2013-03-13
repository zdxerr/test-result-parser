# -*- coding: utf-8 -*-

import os
import cPickle as pickle
from pprint import pprint

path = "E:\\result_analysis"
files = ["crtita_result"]

def load(file_path):
    with open(file_path, "r") as result_file:
        result = pickle.load(result_file)
    return result

if __name__ == '__main__':
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\' \
                  'RTIFlexRay\\Res\\INT13\\T_01_RFT\\TS4\\Result\\' \
                  'crtita_result'
    result = RTITEResultFile(result_path)
    print result
    print result.time
    print result.description

    # pprint(result.environment)
    pprint(result.run)
    pprint(result.sequences)
