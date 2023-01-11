# NAME

revup config - Edit revup configuration files.

# SYNOPSIS

`revup config [--help] [--repo=<repo>] <command> <flag> <value>`

# DESCRIPTION
Revup stores some persistent configuration values in a python configparser
compatible format. A repo specific configuration is read from the root of
the current git repo in a ".revupconfig" file. A user configuration is read
from REVUP_CONFIG_PATH if available, otherwise from the default path of
~/.revupconfig. Keys set in the user config will override the same keys set
in the repo specific config. Any flag or argument to a revup command can
be configured. Revup loads options the following way:

- The program has built in defaults that are given in the manual.
- Revup loads the user's defaults from the config file, which override
the program defaults.
- The user's command line flags can then overwrite any defaults from
either source.

For boolean flags where the default value is "true", the flag can be
negated by prefixing "--no-" to the long form, or "-n" to the short
for if it exists. If several forms of a flag are given on the command
line, the value of the last one will be used.

**Example:**
The default value for `revup upload --skip-confirm` is `false`. The user
can override this by adding this section to .revupconfig.
```
[upload]
skip_confirm = True
```
If the user then wants to temporarily override their config, they can
run `revup upload --no-skip-confirm`.

# OPTIONS

**`<command>`**
: The revup command that the specific configuration applies to. This will
be the same command that contains the help page for this argument. Some
global configuration is under the "revup" section and applies to all
commands.

**`<flag>`**
: The name of the flag to be configured. Dashes will be replaced with
underscores in the underlying file.

**`<value>`**
: The desired value of the flag. Booleans are specified as "true" and "false".

**--help, -h**
: Show this help page.

**--repo, -r**
: If specified, configuration value will only apply for the given git
repository path. Otherwise, value will apply for all git repositories.

# EXAMPLES

Set the user's github username

: $ `revup config revup github-username <username>`

Set the user's github username for a specific repository only

: $ `revup config revup github-username <username> --repo ~/git`
