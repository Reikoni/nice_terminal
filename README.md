# Basic information about the terminal

[English ReadMe](https://github.com/Reikoni/nice_terminal/blob/master/README.md) • [Русский ReadMe](https://github.com/Reikoni/nice_terminal/blob/master/README.ru.md)

**Current version**: Beta

**Nice Terminal** is an open source terminal written in Python without the use of extra libraries.
This terminal makes it easy to write command descriptions and their functionality right in Python!
Nice Terminal currently works only on OS Linux.

## Installation and launch

For Linux:
```sh
git clone https://github.com/Reikoni/nice_terminal
cd nice_terminal
./start
```

## Command syntax:

At the beginning, we specify the name of the command, and then we write the arguments in < >. If you need to write the signs < and > inside the argument, then you need to write /* and */, respectively.

We can also access the desired argument right away, for this you need to find out the full name or abbreviated name of the argument (they are stored in the commands.json file), then write in < >, namely at the beginning of the prefix (it is in the settings.json file in the column preffix), after the argument name we need, a colon and the value of our argument.

**Example:**
```sh
wrt <--line: Hello!>
```
