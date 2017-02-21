"""
Copyright (c) 2017 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals
from __future__ import print_function


def get_config(self, module):
    self.log.info('get_config on {0}'.format(module.__name__))
    self.log.info(module.get_config(self.workspace).cluster_configs)
    self.log.info(module.get_config(self.workspace).conf)
