"""
Copyright (c) 2017 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals
from __future__ import print_function

import json


def log_cluster_configs(cluster_configs):
    configs = {}
    for platform, clusters in cluster_configs.items():
        configs[platform] = [
            {
                'name': cluster.name,
                'max_concurrent_builds': cluster.max_concurrent_builds,
                'enabled': cluster.enabled,
            } for cluster in clusters
        ]

    return json.dumps(configs, indent=4)


def get_config(self, module):
    assert module is not None
    self.log.info('Calling get_config from {0}'.format(module.__name__))

    cluster_configs = module.get_config(self.workflow).cluster_configs
    cluster_configs = log_cluster_configs(cluster_configs)
    self.log.info('get_config().cluster_configs:\n', cluster_configs)

    config = json.dumps(module.get_config(self.workflow).conf, indent=4)
    self.log.info('get_config().config:\n', config)
