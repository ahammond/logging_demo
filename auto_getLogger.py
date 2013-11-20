#!/usr/bin/env python2

from auto_getlogger import *
from logging.config import fileConfig


class A(AutoGetLogger):
    def __init__(self, l=None):
        l.debug('A instantiated')
        l.info('A info')
        l.error('A exploding!!!')

    def my_method(self, l=None):
        l.debug('debug output in my_method')
        l.info('info input in my_method')

    def my_interesting_method(self, l=None):
        l.debug('debug output in my_interesting_method')
        l.info('info input in my_interesting_method')

    def my_noisy_method(self, l=None):
        for x in range(1, 10):
            l.info('noisy %d', x)
        l.error('a real warning message!!!')


class B(A):
    def __init__(self, l=None):
        super(B, self).__init__()
        l.debug('B instantiated')
        l.info('B info')
        l.error('B exploding!!!')

    def my_interesting_method(self, l=None):
        super(B, self).my_interesting_method()
        l.debug('debug output in my_interesting_method')
        l.info('info input in my_interesting_method')


@auto_getlogger
def my_function(l=None):
    l.debug('debug output in my_function')

fileConfig('introspective_logging_config.ini')

c = B()
c.my_method()
c.my_interesting_method()
c.my_noisy_method()
my_function()
