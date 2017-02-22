# Plugin to Inspect Plugins in Atomic Reactor

**WARNING: This is highly experimental! No guaranties whatsoever!**

This Atomic Reactor plugin was born from the need of inspecting
the workflow object accessible by [plugins](https://github.com/projectatomic/atomic-reactor/blob/master/docs/plugins.md).

We also wanted to try functions provided by these plugins.

## Usage

`exit_inspect_plugins.py` and `inspectors.py` should end up in the
`plugins` directory of the `atomic-reactor` installation in your buildroot.

Additional functions to inspect the [workflow object](https://github.com/projectatomic/atomic-reactor/blob/master/docs/plugin_development.md) can be added to `inspectors.py`.

All functions will be attached to the plugin instance and will have access
to `workflow`, `log` and `target` through `self`.

Additionally all calls to the inspector functions will receive as a parameter
the plugin module they inspect. If there is no plugin module name requested,
the module parameter can be `None`.

To enable the exit plugin for a build [osbs-client](https://github.com/projectatomic/osbs-client/) can be [configured](https://github.com/projectatomic/osbs-client/blob/master/docs/configuration_file.md#build-json-templates) to ask for this plugin to be run.

Example configuration placed in `prod_inner.json`s exit plugin section:

```json
{
    "name": "inspect_plugins",
    "required": false,
    "args": {
        "plugins": [
            {
                "name": "pre_reactor_config",
                "inspect_funk": [
                    "get_config"
                ]
            }
        ]
    }
}
```

This will cause the plugin to import `pre_reactor_config` plugin and pass it
to each inspector function specified in `inspector_funk`.

The `plugins` argument is a list, so one can specify multiple plugins to 
inspect.
