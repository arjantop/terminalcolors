# TerminalColors

Utility program for converting vim colorschemes to GNOME Terminal colors

## Howto

### Mapping file

#### Lines in format:

        key=value
        
#### Possible keys:

        background, foreground, bold, black, lblack, red, lred, green, lgreen, yellow, lyellow,
        blue, lblue, cyan, lcyan, purple, lpurple, white, lwhite
        
For pairs [colorname] and l[colorname] at leas one of the two must be set.
If one of them is missing color value is calculate from the other (10% darker than light color or 10% lighter than normal color)

#### Values:

There are two supported value formats:

* Color in hexadecimal notation (#000000)
* Color name from vim colorscheme

        let [a-z]+:%s *= *\"(#[0-9a-fA-F]{6})\"

### Running

        $ python terminalcolors.py path/to/mapping/file path/to/vim/colorscheme
        
If successful, new profile with colors set will be avaliable in Gnome Terminal

### Testing

To see if all the colors are mapped correctly run:

        $ ./colortest.sh

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

    $ python terminalcolors.py color_mapping path/to/hybrid.vim


### Final result

![Vim colorscheme hybrid](https://raw.github.com/arjantop/terminalcolors/master/sample.png)


