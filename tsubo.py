#!/usr/bin/env python3

"""
    Tsubo create random filenames for existing files.
"""

__author__ = 'Christian Buhtz'
__website__ = 'https://github.com/buhtz/tsubo'
__date__ = 'November 2015'
__maintainer__ = __author__
__email__ = 'c.buhtz@posteo.jp'
__license__ = 'GPLv3'
__version__ = '0.0.1a'
__app_name__ = 'Tsubo'

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import string
import os
import glob
import argparse
import random
import subprocess


def _GetFiles(dirs, include):
    """
    """
    files = []

    for d in dirs:
        for i in include:
            files += glob.glob(d + os.sep + i)
    return files

def _CreateArgParser():
    """
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                description='{} {} -- Create random file names out of existing ones.'
                            .format(__app_name__, __version__),
                epilog='  Author:\t{} <{}>\n  Website:\t{}'.format(__author__, __email__, __website__))
    # e.g. '*.mp3' or '*'
    parser.add_argument('include', metavar='INCLUDE_PATTERN', type=str,
                        help='Specify the files to include with a wildcard-mask patter. Enclose it '\
                             'with single quotes to stop bash expanding.\n'\
                             'It can be a list seperated by {}.'.format(os.pathsep))
    # --input-dir, -i
    parser.add_argument('-i', '--input-dir', metavar='DIR', dest='inputDir',
                        default=os.path.abspath(os.curdir), type=str,
                        help='The directory where to start from (default: current working directory).')
    # --output-dir
    # TODO: create output-dir if it doesn't exists
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o', '--output-dir', metavar='DIR', dest='outputDir', type=str,
                       help='Use the specified directory for output.')
    group.add_argument('--output-to-cwd', dest='outputCwd', action='store_true',
                       help='Use the current working directory as output directory.')
    group.add_argument('--output-to-input', dest='outputIn', action='store_true',
                       help='Use the given input directory (or the first in the list) as output directory.')

    # --recursive, -r, -R
    parser.add_argument('-r', '--recursive', action='store_true', dest='argRecursiv',
                       help='Do the job recursivly through the sub-directories.')

    # --action
    parser.add_argument('--action', metavar='CMD', dest='action', type=str,
                        help='Use this with care! Will execute CMD given the original filename as '\
                        'first and the new filename as second argument.')
    # --no-rm-security-question
    parser.add_argument('--no-rm-security-question', action='store_true', dest='noaskRM',
                        help='')
    # --no-mv-security-question
    parser.add_argument('--no-mv-security-question', action='store_true', dest='noaskMV',
                        help='')
    # --no-progress
    parser.add_argument('--no-progress', action='store_true', dest='noProgress',
                        help='Supress progress messages while --action is called.')

    # outfile
    # TODO
    # --sperator (default ;)
    # --prefix, e.g. PREFIX0001.mp3
    # --postfix, e.g. 0001POSTFIX.mp3
    return parser


def _askForAction(a):
    """
    """
    q = 'ATTENTION: Your action include "{}". You should use that with care.\n'\
        'Are you really sure that you want to execute this action on each file?\n'\
        'The actions is: "{}"\n'\
        'Type "yes" if it is so: '.format(a, action)

    if input(q).lower() == 'yes':
        return True
    else:
        return False


def _actionSTDOUT(org, new):
    """
    """
    print('{};{}'.format(org, new))


def _actionUser(org, new):
    """
    """
    cmd = action.split()
    cmd += [org]
    cmd += [new]
    subprocess.check_call(cmd)


if __name__ == '__main__':
    # commandline arguments
    parser = _CreateArgParser()
    # store all arguments in objects/variables of the local namespace
    locals().update(vars(parser.parse_args()))

    # prepare
    include = include.split(os.pathsep)
    rootDir = os.path.expanduser(os.path.normpath(inputDir))
    orgFiles = []
    inputDirs = [rootDir]

    # output directory
    if outputCwd:
        # current working directory for output
        outputDir = os.path.abspath(os.curdir)
    elif outputIn:
        # current input directory for output
        outputDir = inputDirs[0]
    else:
        if outputDir:
            # user (per argument) specified directory for output
            outputDir = os.path.expanduser(os.path.normpath(outputDir))

    # recursive?
    if argRecursiv == True:
        for root, dirs, names in os.walk(rootDir):
            # hidden directory?
            if '{}.'.format(os.sep) in root:
                continue
            # still in?
            if root in inputDirs:
                continue
            # use it
            inputDirs += [root]

    # create a list of each related file
    orgFiles += _GetFiles(inputDirs, include)

    # random ordered unique numbers
    randNumbers = list(range(0, len(orgFiles)))
    random.shuffle(randNumbers)

    newFiles = []
    alph = string.ascii_letters[random.randrange(0, len(string.ascii_letters)-1)]
    formatStr = '{:0' + str(1+len(str(len(orgFiles)))) + '}'

    # pair the original files with its new names (incl. the absoulute paths) in a tuple
    for org, rnd in zip(orgFiles, randNumbers):
        org_name, org_ext = os.path.splitext(org)
        org_name = org_name.rsplit(os.sep, 1)[0]

        # create new filename
        newFiles += [ (outputDir if outputDir else org_name) + os.sep + alph + formatStr.format(rnd) + org_ext ]

    # are their files
    if len(orgFiles) == 0:
        print('No files found.')
        sys.exit()

    # TODO to outfile

    actionDo = None

    # do an action?
    if action:
        action = action.replace("'", "")
        action = action.replace('"', '')
        if 'rm' in action and not noaskRM:
            if _askForAction('rm') != True: sys.exit()
        if 'mv' in action and not noaskMV:
            if _askForAction('mv') != True: sys.exit()

        actionDo = _actionUser

    else:
        # to STDOUT
        actionDo = _actionSTDOUT

    count = 1
    maxCount = len(orgFiles)
    pPercent = 100 / maxCount
    progress = True if not noProgress and actionDo is _actionUser else False

    for org, new in zip(orgFiles, newFiles):
        # progress
        if progress:
            print('File {} of {} ({}%)..'.format(count, maxCount, int(pPercent*count)), end='\r')
        # action
        actionDo(org, new)
        count += 1

    if progress: print('\n')

    sys.exit()

