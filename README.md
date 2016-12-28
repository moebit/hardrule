## Hardrule
Current version of pfSense's _easyrule_ does not include any options for port forwarding. This script is an example of directly modifying `config.xml` for port forwarding. The major take away is after each modification, the config cache file which is located at `/tmp/config.cache` should be removed and `/etc/rc.interfaces_wan_configure` must be run. Both of these steps are executed in `update()` function.

### Usage
- In pfSense: Copy the script into `/cf/conf` 
- `add` or `delete` rules using `python hardrule.py {add,delete}`. All changes will be immediately applied.
- To get more information on subcommands use `python hardrule.py {add,delete} --help`

### Note
This script was part of the dynamic port assignment concept and can be customized for any automated purpose.
