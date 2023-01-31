# Initialize pretty printer at startup

Setup system-wide gdbinit. Init file should be located at '/etc/gdb/gdbinit'.
Append folowing lines:

``` bash
add-auto-load-safe-path ~/.config/gdb/.gdbinit # enables to use file from other location
source ~/.config/gdb/.gdbinit # will use file specified at each startup
```

Then create .gdbinit file in home directory.

``` bash
mkdir ~/.config/gdb
touch ~/.config/gdb/.gdbinit
```

Append to .gdbinit in home directory.

``` bash
source <path to printer script>
```

Pretty printer should now be loaded each time gdb is launched.
