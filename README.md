### TT-PyShell ###

### Developed in Python version 3.14.2 ###
#### Requires Python 3.10+, cURL, Git and Linux for full functionality ####

A Python shell with a few useful features built around OS libraries, subprocesses, and other Python libraries. It uses `shlex` for parsing and includes wrappers for tools like Git and cURL. Mostly built as a learning project, but it's also usable for actual command-line work and easy to mess around with if you want to add your own features.


## TTShell

### Setup guide

*Clone this repo*

```
git clone https://github.com/TatuPekkarinen/c

```

*Pip install requirements.txt*

```
pip install -r requirements.txt

```

*Then just run the script main.py*
```
For the working directory of the shell
[/-/-/shell/TT-PyShell] 
python main.py

```



### Initial interface
```
tt-shell / <timestamp>
Network Status >> <status>
[/path/to/tt-shell-python/main.py] >>> 

```



### Connection Commands
*Single Port Connection*
```
[/path/to/tt-shell-python/main.py] >>> con <host> <port>
connecting to <host_ip> from <port>
Port / <port> / RESPONDED
```
*Ranged Localhost Port Scan*
```
[/path/to/tt-shell-python/main.py] >>> con range <start_port> <end_port>
Starting scan from <start_port> to <end_port>
Port / 1 / CONNECTION REFUSED
Port / 2 / CONNECTION REFUSED

```


### Type Command
*Checks if a command is builtin or a system executable*
```
[/path/to/tt-shell-python/main.py] >>> type <command>
<command> >>> <path or function info>

```

```
[/path/to/tt-shell-python/main.py] >>> type echo
echo // <function reference>

[/path/to/tt-shell-python/main.py] >>> type konsole
konsole >>> /usr/bin/konsole
```



### Echo Command
*Prints text to the shell*
```
[/path/to/tt-shell-python/main.py] >>> echo "Hello world!"
Hello world!
```



### Web Command
*Opens a website and checks connectivity*
```
[/path/to/tt-shell-python/main.py] >>> web <website>
CONNECTION TEST >>> Connection to <host_ip> from <443>
CONNECTION SUCCESSFUL >>> Accessing website / <website>
```



### File Execution
*Runs a system file*
```
[/path/to/tt-shell-python/main.py] >>> file <filename>
Opening file >>> <path_to_file>
```



### Change directory
*changes current working directory*
```
[/home/--/shell/tt-shell-python] >>> change /home
[/home] >>> change reset
[/home/--/shell/tt-shell-python] >>>
```



### Command History
*View and clear past commands*
```
[/path/to/tt-shell-python/main.py] >>> history
Command history
>>> <past commands>
```

```
[/path/to/tt-shell-python/main.py] >>> history clear
```



### Git Commands
*Supports Git commands via wrapper*

```
[/path/to/tt-shell-python/main.py] >>> git
usage: git <command> [<args>]
Common Git commands:
  clone, init, add, mv, restore, rm, bisect, diff, grep, log, show, status,
  backfill, branch, commit, merge, rebase, reset, switch, tag, fetch, pull, push
```



### cURL Wrapper
*Supports curl commands*
```
[/path/to/tt-shell-python/main.py] >>> curl <url>
### Example:
[/path/to/tt-shell-python/main.py] >>> curl google.com
<HTML>...
<TITLE>301 Moved</TITLE>
...
```



### Debugging Commands
*Lists all available commands*
```
[/path/to/tt-shell-python/main.py] >>> com
{
 'com': <function>,
 'con': <function>,
 'curl': <function>,
 'echo': <function>,
 'env': <function>,
 'exit': <function>,
 'file': <function>,
 'git': <function>,
 'history': <function>,
 'morph': <function>,
 'python': <function>,
 'type': <function>,
 'web': <function>
}
```
*Displays environment variables*
```
[/path/to/tt-shell-python/main.py] >>> env
{
 'HOME': '<user_home>',
 'PATH': '<env_paths>',
 'SHELL': '/usr/bin/bash',
 'USER': '<username>',
 'VIRTUAL_ENV': '<venv_path>',
 ...
}
```
*Displays current python version*
```
[/path/to/tt-shell-python/main.py] >>> python
[/path/to/tt-shell-python/main.py] >>> {python version}
```
