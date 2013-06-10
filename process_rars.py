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
import tempfile
import shutil

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
    parser.add_argument('--source', '-s', help="File location directory (default: '%s')" \
                        % default_source_dir,
                        default=default_source_dir)
    parser.add_argument('--dest', '-d', help='File destination directory',
                        default=default_dest_dir)
    parser.add_argument('--password', '-P', help='RAR file password', required=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Prints out extra information (default: false)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + version)

    args = parser.parse_args()
    return args


def main():

    args = get_args()

    if not os.path.exists(args.source):
        raise Exception("Directory %s doesn't exist!" % args.source)

    flag_file_name = os.path.join(tempfile.gettempdir(), 'crc-check-is-running.mvg')
    if os.path.exists(flag_file_name):
        raise Exception("Process is already running ...")

    flag = open(flag_file_name,'w')
    print >>flag, datetime.datetime.now()
    flag.close()

    # data source:
    source = os.path.abspath(args.source)
    # List of RAR files:
    source = [source] if os.path.isfile(source) else set(
                glob.glob(os.path.join(source, '*.rar'))
                + glob.glob(os.path.join(source, '*.RAR'))
             )

    # loop via found files
    for fn in source:
        #  1. Check this folder for all .rar files
        #  2. Copy file into a temporary file folder
        bfn = os.path.basename(fn)  # base file name
        if args.verbose:
            print "* Processing file '%s'" % bfn
        cfn = os.path.join(tempfile.gettempdir(), bfn)  # compy file name
        shutil.copyfile(fn, cfn)

        #  3. CRC check all .rar files:
        options =""
        if args.password != "":
            options += " -p"+args.password
        unrar_test_cmd = "unrar t %s %s" % (options,cfn)
        unrar_test = os.popen(unrar_test_cmd)
        # last line is "All OK"
        is_all_ok = (unrar_test.read().splitlines()[-1] == 'All OK')
        #  4. If file is corrupted .rar file gets deleted.
        if not is_all_ok:
            print "* File", fn, "is corrupted..."
            #  5. Each rar file has a two additional files
            #     that also gets deleted if file is corrupt.
            fname = os.path.splitext(fn)[0]  # file name w/o extension
            for fe in ['.rar', '.mvg', '.id']:  # file extension to delete
                try:
                    fn_ = fname + fe
                    os.remove(fn_)
                    print "** '%s' deleted" % fn_
                except:
                    print "ERROR: couln't delete file '%s'" % fn_
        elif args.verbose:
            print "* File", fn, "is valid..."

        os.remove(flag_file_name)

if __name__ == '__main__':
    main()
