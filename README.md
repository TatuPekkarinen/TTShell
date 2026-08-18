# mini-pyshell

A small interactive shell written in Python. Uses shlex for parsing and subprocess for execution. Commands in one monolith. 
Built to learn how the standard library and socket connections work, and usable as a real shell along the way.

## Requirements

- Python 3.10+ (developed on 3.14.2)
- Linux
- `git`, `curl`

## Install

```
git clone https://github.com/TatuPekkarinen/mini-pyshell
cd mini-pyshell
pip install -r requirements.txt
python main.py
```

## Commands

| Command | Description |
| --- | --- |
| `con <host> <port>` | Test a single TCP port |
| `con range <start> <end>` | Scan a localhost port range |
| `type <command>` | Show whether a command is builtin or a system executable |
| `echo <text>` | Print text |
| `web <url>` | Check connectivity, then open the site |
| `file <path>` | Run a system file |
| `change <path>` | Change working directory (`change reset` to return) |
| `history` | Show past commands (`history clear` to wipe) |
| `git <args>` | Git wrapper |
| `curl <args>` | cURL wrapper |
| `com` | List available commands |
| `env` | List environment variables |
| `python` | Show the running Python version |
| `exit` | Quit |

## Startup

```
mini-pyshell / <timestamp>
Network Status >> <status>
[~/mini-pyshell] >>>
```

## Examples

### Connections

```
[~/mini-pyshell] >>> con <host> <port>
connecting to <host_ip> from <port>
Port / <port> / RESPONDED

[~/mini-pyshell] >>> con range 1 2
Starting scan from 1 to 2
Port / 1 / CONNECTION REFUSED
Port / 2 / CONNECTION REFUSED
```

### Type

```
[~/mini-pyshell] >>> type echo
echo // <function reference>

[~/mini-pyshell] >>> type konsole
konsole >>> /usr/bin/konsole
```

### Echo

```
[~/mini-pyshell] >>> echo "Hello world!"
Hello world!
```

### Web

```
[~/mini-pyshell] >>> web <website>
CONNECTION TEST >>> Connection to <host_ip> from <443>
CONNECTION SUCCESSFUL >>> Accessing website / <website>
```

### File

```
[~/mini-pyshell] >>> file <filename>
Opening file >>> <path_to_file>
```

### Change directory

```
[~/mini-pyshell] >>> change /home
[/home] >>> change reset
[~/mini-pyshell] >>>
```

### History

```
[~/mini-pyshell] >>> history
Command history
>>> <past commands>

[~/mini-pyshell] >>> history clear
```

### Git

```
[~/mini-pyshell] >>> git
usage: git <command> [<args>]
Common Git commands:
  clone, init, add, mv, restore, rm, bisect, diff, grep, log, show, status,
  backfill, branch, commit, merge, rebase, reset, switch, tag, fetch, pull, push
```

### cURL

```
[~/mini-pyshell] >>> curl google.com
<HTML>...
<TITLE>301 Moved</TITLE>
...
```

### Misc

```
[~/mini-pyshell] >>> com
{'com': <function>, 'con': <function>, 'curl': <function>, 'echo': <function>,
 'env': <function>, 'exit': <function>, 'file': <function>, 'git': <function>,
 'history': <function>, 'morph': <function>, 'python': <function>,
 'type': <function>, 'web': <function>}

[~/mini-pyshell] >>> env
{'HOME': '<user_home>', 'PATH': '<env_paths>', 'SHELL': '/usr/bin/bash',
 'USER': '<username>', 'VIRTUAL_ENV': '<venv_path>', ...}

[~/mini-pyshell] >>> python
3.14.2
```

## License

MIT
