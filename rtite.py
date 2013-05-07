# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
from operator import itemgetter
import dateutil.parser
from pprint import pprint
import logging

import scipy.io.matlab

from result import ResultFile, Sequence

SWVER_PARAMS = [
    'compiler',
    'matlab_java',
    'matlab_long',
    'matlab_short',
    'operating_system',
    'test_environment',
    'packageversion',
    'rapidpro_info',
    #'dslicense',
    #'matlab_arch'
]

SWROOT_PARAMS = [
    'dspace',
    'matlab',
    'tetools',
    'tstools'
]

POSSIBLE_STATES = {
    -3: "Withdrawn",
    -2: "Excluded",
    -1: "Not Executed",
    0: "Ok",
    1: "Fail",
    2: "Fail",
    3: "Fail",
    4: "Fail",
    5: "Fail",
}


def datenum_to_datetime(datenum):
    """Convert Matlab datenum (days since the 01.01.0000) to datetime."""
    return (datetime.fromordinal(int(datenum)) -
            timedelta(days=366) +
            timedelta(days=datenum % 1))


class RTITEResult(ResultFile):
    @property
    def td(self):
        return self.__td

    def parse(self):
        self.__mat = scipy.io.matlab.loadmat(self.path)
        self.__td = self.__mat['testdata']

        # add platform to tags
        # self.tags.append(os.path.basename(self.path).split('_')[-1][:-4])
        self.nodes.append('RTITE')

        self.__parse_environment()
        self.__parse_run()

        self.__parse_sequences()

    def __parse_environment(self):
        self.environment = environment = {}
        env = self.__td['environment'][0][0][0]

        swver = environment['swver'] = {}
        for p in SWVER_PARAMS:
            try:
                swver[p] = env['swver'][0][0][0][p][0]
            except:
                # some parameters are not available in older test results
                logging.debug("Unable to parse parameter `{}` no found.", p)

        swroot = environment['swroot'] = {}
        for p in SWROOT_PARAMS:
            swroot[p] = env['swroot'][0][0][0][p][0]

        getter = itemgetter('Name', 'Version', 'SP', 'Addresswidth')
        os = map(lambda i: i[0][0][0],
                 getter(env['wmic_sysinfo'][0]['os'][0][0]))
        self.os = '{} {} ({}) {}bit'.format(*os)

        self.pc = env['wmic_sysinfo'][0]['net'][0][0]['name'][0][0][0]
        self.platform = swver['test_environment']

    def __parse_run(self):
        self.run = run = {}

        try:
            self.description = self.__td["teparam"][0][0][0][0]["comment"][0]
        except:
            pass

        result = self.__td[0]['result'][0]

        # time_format = "%d-%b-%Y %H:%M:%S"
        self.start = dateutil.parser.parse(result['time_start'][0][0][0],
                                           dayfirst=True, fuzzy=True)
        self.end = dateutil.parser.parse(result['time_finish'][0][0][0],
                                         dayfirst=True, fuzzy=True)

        run["repeated_failed_tests"] = ""
        run["excluded_tests"] = []
        try:
            run["repeated_failed_tests"] = \
                self.__td[0]["teparam"][0]["repeat_failed_tests"][0][0][0]
            run["excluded_tests"] = [
                t[0] for t in
                self.__td["teparam"][0][0][0][0]["really_excluded_tests"][0]]
            run["excluded_tests"] += [
                t[0] for t in
                self.__td["teparam"][0][0][0][0]["unused_excluded_tests"][0]]
        except IndexError:
            pass

    def __parse_sequences(self):
        self.sequences = sequences = []
        for script in self.__td[0]['result'][0]['script'][0][0][0]:
            s = RTITESequence(script['name'][0], int(script['status'][0][0]))

            d = script['name'][0].split('\\')
            s.name = d[-1]
            s.group = d[-2]
            s.nodes = d[:-2]

            try:
                s.comment = script["comment"][0]
            except:
                pass

            # read and convert timestamps
            dc = script['datacollector'][0]
            timestamps = []
            for i in [0, 2, 3, 4, 5, 7]:
                try:
                    ts = datenum_to_datetime(dc[i]['collect_time'][0][0][0][0])
                except:
                    ts = None
                finally:
                    timestamps.append(ts)

            s.start, s.end = timestamps[0], timestamps[-1]

            s.test_depth_max = int(script['test_depth_max'][0][0])
            s.test_depth_executed = int(script['test_depth_executed'][0][0])

            teststage = int(script['error']['teststage_failed'][0][0][0][0])
            s.teststage_failed = None if teststage == -1 else teststage

            for n, msg in enumerate(script['stage_info']['output'][0]):
                try:
                    s.log.append(
                        {
                            'id': n,
                            'status': 1 if teststage == n else 0,
                            'message': '\n'.join(
                                l.strip() for l in msg[0].split('\n')
                                if l.strip()),
                            'name': "Stage {}".format(n),
                            'timestamp': timestamps[n]
                        }
                    )
                    logging.debug("Appended log for stage {}".format(n))
                except Exception, exc:
                    # logging.warn("Failed to append log for stage {}".format(n))
                    # logging.warn(exc)
                    pass

            s.errors = []
            try:
                for testcase in script['error']['testcase'][0][0][0]:
                    s.errors.append({
                        'messages': testcase['msg'].tolist(),
                        'number': int(testcase['number'][0][0]),
                        'state': testcase['state'][0],
                        'stage': int(testcase['stage'][0][0])
                    })
            except IndexError:
                pass

            sequences.append(s)


class RTITESequence(Sequence):
    possible_states = {
        -3: "Withdrawn",
        -2: "Excluded",
        -1: "Not Executed",
        0: "Ok",
        1: "Fail",
        2: "Fail",
        3: "Fail",
        4: "Fail",
        5: "Fail",
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    result_path = 'R:\\PE\\Testdata\\CRTI-Test\\ImplSW_RLS_2013-A\\RTIxxxMM' \
                  '\\Res\\INT17\\T_01\\ts_results_rti1005.mat'
    result = RTITEResult(result_path)

    for s in result.sequences:
        if s.state == "Fail":
            print s.id,
            print s.name, s.nodes,
            print s.end - s.start

    # pprint(result.environment)
    # pprint(result.run)
    #pprint(result.sequences)
