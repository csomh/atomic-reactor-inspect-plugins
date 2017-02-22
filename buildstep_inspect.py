"""
Copyright (c) 2017 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals
from __future__ import print_function

from atomic_reactor.plugin import BuildStepPlugin, InappropriateBuildStepError
from atomic_reactor.build import BuildResult


class BuildStepInspectPlugin(BuildStepPlugin):
    """
    Log the inputs to the build-step plugin
    """

    key = 'buildstep_inspect'

    def __init__(self, tasker, workflow, fail_reason=None, image_id=None,
                 inappropriate=False):
        """
        """
        super(BuildStepInspectPlugin, self).__init__(tasker, workflow)

        logs = [
            "Step 1 : FROM sha256:<...>",
            "---> <...>",
            "Step 2 : CMD /bin/bash",
            "---> Running in <...>",
            "---> <...>",
            "Removing intermediate container <...>",
        ]

        if image_id is not None:
            final_line = "Successfully built {}".format(image_id)
        else:
            final_line = "Build failed"

        logs.append(final_line)
        self.build_result = BuildResult(logs=logs,
                                        fail_reason=fail_reason,
                                        image_id=image_id)
        self.inappropriate = inappropriate

    def run(self):
        """
        Run plugin, logging self.workflow.builder information
        """

        for line in [
                "Build directory: {}".format(self.workflow.builder.df_dir),
                "Dockerfile path: {}".format(self.workflow.builder.df_path),
                "Image to build: {}".format(self.workflow.builder.image),
                ]:
            self.log.info(line)

        if self.inappropriate:
            self.log.info("Raising InappropriateBuildStepError")
            raise InappropriateBuildStepError

        return self.build_result
