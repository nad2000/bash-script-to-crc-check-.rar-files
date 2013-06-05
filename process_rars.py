#!/usr/bin/env python
#------------------------------------------------------------------------------
# Name:     process_rars
# Purpose:  un-rars *.rar files in the specified directory and verifies them
#
# Author:   Radomirs Cirskis
#
# Created:  05/06/2013
# Licence:  WTFPL
#------------------------------------------------------------------------------

import argparse
import os
import glob

# Constants:
version = '0.1'
default_source_dir = '/DMDS/9.Vuze/1.Share'  # Default file location directry
default_dest_dir   = default_source_dir      # Default destination directory


def get_args():
    """
    Command argument parser

    Returns structure:
        args.source  - file location directory
        args.destr   - destination directory
        args.verbose - prints SQL query

    """

    parser = argparse.ArgumentParser(description='RAR validation',
                                     conflict_handler='resolve')
    parser.add_argument('--source', '-s', help='File location directory',
                        default=default_source_dir)
    parser.add_argument('--dest', '-d', help='File destination directory',
                        default=default_dest_dir)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Prints out extra information (default: false)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)

    args = parser.parse_args()
    return args


def main():
    """
    """
    args = get_args()

    if not os.path.exists(args.source):
            raise Exception("File or directory %s doesn't exist!" % args.input)

    # data source:
    source = os.path.abspath(args.source)
    # List of RAR files:
    source = [source] if os.path.isfile(source) else set(
                glob.glob(os.path.join(source, '*.rar'))
                + glob.glob(os.path.join(source, '*.RAR'))
            )

    # loop via found files
    #  1. Check this folder for all .rar files: `/DMDS/9.Vuze/1.Share/*.rar`
    #  2. Copies all files into a temporary file folder
    #  3. CRC check all .rar files:
    #  4. If file is corrupted .rar file gets deleted.
    #  5. Each rar file has a two additional files that also gets deleted if file I corrupt.

if __name__ == '__main__':
    main()
