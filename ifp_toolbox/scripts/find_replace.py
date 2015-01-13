import os
import os.path
import re
from termcolor import colored


def find_replace(head_folder, search_string, replacement_string=None):

    """
    A function to recursively find (and optionally replace) a string
    pattern in a folder and all of its sub-folders.

    Keyword arguments:
    head_folder --  top-level directory to start search
    search_string -- string pattern to match
    replacement_string -- if specified, string pattern to replace search_string
                          (default: None)
    """

    for root, dirs, files in os.walk(head_folder):
        print colored('In: ', 'cyan', attrs=['bold']), '%s' % root
        if dirs:
            print colored('Directories: ', 'magenta',  attrs=['bold']), \
                '%s\n' % dirs

        for filename in files:
            if not filename.endswith('.py'):
                continue

            print colored('File: ', 'magenta', attrs=['bold']), \
                '%s' % filename

            file_path = os.path.join(root, filename)
            find_replace_for_file(file_path, search_string, replacement_string)


def find_replace_for_file(file_path, search_string, replacement_string):
    lines = read_lines_from_file(file_path)

    match_indices = find_match_locations(lines, search_string)

    display_matches(lines, match_indices, search_string)

    if replacement_string:
        replace_matches(lines, match_indices, search_string,
                        replacement_string)
        write_lines_to_file(file_path, lines)
        print ''


def find_match_locations(lines, search_string):
    match_lines = [re.search(search_string, l) for l in lines]
    match_indices = [i for i, m in enumerate(match_lines) if m]
    return match_indices


def display_matches(lines, match_indices, search_string):
    for i in match_indices:
        out_line = lines[i].rstrip()
        out_line = out_line.replace(search_string, colored(search_string,
                                                           'red',
                                                           attrs=['bold']))
        print colored('Match found', 'red', attrs=['bold']), \
            'in line %d: %s' % (i+1, out_line)

    print ''


def replace_matches(lines, match_indices, search_string, replacement_string):
    for i in match_indices:
        out_line_before = lines[i].rstrip()
        out_line_before = out_line_before.replace(search_string,
                                                  colored(search_string, 'red',
                                                          attrs=['bold']))
        print colored('Replacing ', 'red', attrs=['bold']), \
            'line %d: %s' % (i+1, out_line_before)

        lines[i] = lines[i].replace(search_string, replacement_string)

        out_line_after = lines[i].replace(replacement_string,
                                          colored(replacement_string,
                                                  'green', attrs=['bold']))
        print colored('With:', 'green', attrs=['bold']), ' %s' % out_line_after


def read_lines_from_file(file_path):
    f_read = open(file_path, 'rb')
    lines = f_read.readlines()
    f_read.close()
    return lines


def write_lines_to_file(file_path, lines):
    f_write = open(file_path, 'wb')
    f_write.writelines(lines)
    f_write.close()
