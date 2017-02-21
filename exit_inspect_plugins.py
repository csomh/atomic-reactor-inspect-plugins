"""
Copyright (c) 2017 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals
from __future__ import print_function

from atomic_reactor.plugin import ExitPlugin

import inspectors
import types

try:
    from importlib import import_module
except ImportError:
    import_module = __import__  # 2.6

AR_PLUGINS = 'atomic_reactor.plugins'


class InspectPlugins(ExitPlugin):
    """
    Log the workspace object of a plugin
    """

    key = 'inspect_plugins'
    is_allowed_to_fail = True

    def __init__(self, tasker, workflow, plugins):
        """
        TODO: docs
        plugins = [
            {
                'name': 'post_compress',
                'inspect_funk': 'get_config'
            }
        ]
        """
        super(InspectPlugins, self).__init__(tasker, workflow)

        self.plugins = plugins

    def load(self, plugin):

        name = '.'.join([AR_PLUGINS, plugin['name']])

        self.log.debug('trying to import module {0} ...'.format(name))
        try:
            module = import_module(name)
        except ImportError:
            return None

        return module

    def log_calls(self, module, inspect_funk):
        for funk in inspect_funk:
            try:
                function = getattr(inspectors, funk)
            except AttributeError:
                self.log.error('No such inspector function: {0}'.format(funk))
                continue

            self.function = types.MethodType(function, self)
            self.function(module)

    def run(self):
        """
        Run plugin and log workspeces for the required plugins
        """

        for plugin in self.plugins:

            plugin_module = self.load(plugin)
            if plugin_module is not None:
                self.log_calls(plugin_module, plugin['inspect_funk'])
