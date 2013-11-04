#!/usr/bin/env python3

from inspect import stack as inspect_stack
from logging import getLogger
from logging.config import fileConfig


class A(object):
    def __init__(self):
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        l.debug('A instantiated')
        l.info('A info')
        l.error('A exploding!!!')

    def my_method(self):
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        l.debug('debug output in my_method')
        l.info('info input in my_method')

    def my_interesting_method(self):
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        l.debug('debug output in my_interesting_method')
        l.info('info input in my_interesting_method')

    def my_noisy_method(self):
        l = getLogger("{}.{}".format(self.__class__.__name__, inspect_stack()[0][3]))
        for x in range(1, 10):
            l.info('noisy %d', x)
        l.error('a real warning message!!!')


class B(A):
    def __init__(self):
        super(B, self).__init__()
        l = getLogger('{}.{}'.format(self.__class__.__name__, inspect_stack()[0][3]))
        l.debug('B instantiated')
        l.info('B info')
        l.error('B exploding!!!')

    def my_interesting_method(self):
        super(B, self).my_interesting_method()
        l = getLogger('{}.{}'.format(self.__class__.__name__, inspect_stack()[0][3]))
        l.debug('debug output in my_interesting_method')
        l.info('info input in my_interesting_method')

fileConfig('introspective_logging_config.ini')

c = B()
c.my_method()
c.my_interesting_method()
c.my_noisy_method()
