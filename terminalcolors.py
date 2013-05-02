#!/usr/bin/env python

import sys
import re
import gconf
from os.path import splitext, basename
import colorsys

term_colors = ["background", "foreground", "bold", "black", "lblack",
               "red", "lred", "green", "lgreen", "yellow", "lyellow",
               "blue", "lblue", "cyan", "lcyan", "purple", "lpurple",
               "white", "lwhite"]


def read_line(line):
    [key, val] = line.split("=")
    return (key, val)


def read_mapping(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    return dict([read_line(line.strip()) for line in lines])


def find_color(text, color_name):
    pattern = "let [a-z]+:%s *= *\"(#[0-9a-fA-F]{6})\"" % color_name
    matches = re.search(pattern, text)
    return hex2rgb(matches.group(1))


def hex2rgb(s):
    s = s[1:]
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def rgb_brighten(color, mul):
    (h, l, s) = colorsys.rgb_to_hls(*[c / 255.0 for c in color])
    rgb_float = colorsys.hls_to_rgb(h, max(0, min(1, l * mul)), s)
    return tuple([int(x * 255) for x in rgb_float])


def int2hex8(n):
    h = hex(n)[2:]
    return h if len(h) is 2 else "0" + h


def rgb2hex16(color):
    parts = [int2hex8(c) * 2 for c in color]
    return "#" + "".join(parts)


def gconf_set_string(client, path, name, value):
    client.set_string(path + name, value)


def gconf_set_bool(client, path, name, value):
    client.set_bool(path + name, value)


def gconf_set(client, path, settings):
    for key, value in settings.iteritems():
        if type(value) is str:
            gconf_set_string(client, path, key, value)
        elif type(value) is bool:
            gconf_set_bool(client, path, key, value)


def palette(colors):
    p = [colors["black"], colors["red"], colors["green"], colors["yellow"],
         colors["blue"], colors["cyan"], colors["purple"], colors["white"]]
    lp = [colors["lblack"], colors["lred"], colors["lgreen"],
          colors["lyellow"], colors["lblue"], colors["lcyan"],
          colors["lpurple"], colors["lwhite"]]
    return ":".join(rgb2hex16(c) for c in p + lp)


def expand(text, mapping):
    if mapping[0] is '#':
        return hex2rgb(mapping)
    else:
        return find_color(text, mapping)


def expand_mappings(text, mapping):
    colors = {}
    for tc in term_colors:
        if tc in mapping:
            colors[tc] = expand(text, mapping[tc])
        elif tc[0] is 'l' and tc[1:] in mapping:
            colors[tc] = rgb_brighten(expand(text, mapping[tc[1:]]), 1.1)
        elif 'l' + tc in mapping:
            colors[tc] = rgb_brighten(expand(text, mapping['l' + tc]), 0.9)
        else:
            raise Exception("No mapping for color %s found" % tc)
    return colors


if __name__ == "__main__":
    if len(sys.argv) is not 3:
        print "Usage: terminalcolors.py [mapping_file] [vim_colorscheme]"
        exit()
    mapping_file, vim_file = sys.argv[1], sys.argv[2]
    mapping = read_mapping(mapping_file)
    file_contents = open(vim_file, 'r').read()
    colors = expand_mappings(file_contents, mapping)
    name = re.sub("[^a-zA-Z]", '', splitext(basename(vim_file))[0])
    client = gconf.client_get_default()
    gtp = "/apps/gnome-terminal/"
    profile_list_path = gtp + "global/profile_list"
    profile_path = gtp + "profiles/%s/" % name
    settings = {
        "visible_name": name,
        "use_theme_background": False,
        "use_theme_colors": False,
        "bold_color_same_as_fg": False,
        "background_color": rgb2hex16(colors["background"]),
        "foreground_color": rgb2hex16(colors["foreground"]),
        "bold_color": rgb2hex16(colors["bold"]),
        "palette": palette(colors)
    }
    profile_list = client.get_list(profile_list_path, gconf.VALUE_STRING)
    if name not in profile_list:
        profile_list.append(name)
        client.set_list(profile_list_path, gconf.VALUE_STRING, profile_list)
    gconf_set(client, profile_path, settings)
