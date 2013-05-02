# TerminalColors

Utility program for converting vim colorschemes to GNOME Terminal colors

## Example

Conversion of vim coloscheme [hybrid](https://github.com/w0ng/vim-hybrid)

### Mapping file

[color_mapping](https://raw.github.com/arjantop/terminalcolors/master/color_mapping):
```
background=background
foreground=foreground
bold=aqua
black=#000000
lblack=#666666
red=red
green=green
yellow=yellow
blue=blue
cyan=aqua
purple=purple
white=#929395
```

### Command

    $ python terminalcolors.py color_mapping path/to/colorscheme.vim


### Final result

    $ ./colortest.sh

![Vim colorscheme hybrid](https://raw.github.com/arjantop/terminalcolors/master/sample.png)


