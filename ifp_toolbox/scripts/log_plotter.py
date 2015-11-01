import os
import argparse
import re
from glob import glob

import numpy
from matplotlib import pyplot


class DataObject(object):
    def __init__(self, file_pattern, log_pattern):
        self.files = glob(file_pattern)
        self.regex = re.compile(log_pattern)

        self.data_dict = {}
        for file in self.files:
            with open(file, 'r') as f:
                lines = f.readlines()
            matches = numpy.float32(numpy.array([self.regex.findall(line)[0] for line in lines if self.regex.findall(line)]))
            self.data_dict[file] = matches

    def plot(self):
        for key, value in self.data_dict.iteritems():
            pyplot.plot(value, label=key)

        pyplot.legend()
        pyplot.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='log plotter',
                                     description='Script to plot log data.')

    parser.add_argument('file_pattern', help='Pattern for matching log files.')
    parser.add_argument('log_pattern', help='Pattern for getting data values.')

    args = parser.parse_args()

    # file_pattern = '*.txt'
    # log_pattern = '[0-9] (.*)'
    do = DataObject(args.file_pattern, args.log_pattern)
    do.plot()