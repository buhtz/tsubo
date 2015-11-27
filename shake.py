#!/usr/bin/env python3

"""
    SHAKE create random filenames for existing files.
"""

__author__ = 'Christian Buhtz'
__date__ = 'November 2015'
__maintainer__ = __author__
__email__ = 'c.buhtz@posteo.jp'
__license__ = 'GPLv3'
__version__ = '0.0.1a'
__app_name__ = 'SHAKE'

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
import os
import glob
import argparse
import random


def _GetFiles(dirs, include):
    """
    """
    files = []

    for d in dirs:
        for i in include:
            files += glob.glob(d + os.sep + i)
    return files


if __name__ == '__main__':
    # read commandline arguments
    parser = argparse.ArgumentParser(
                description='{} {} -- Create random file names out of existing ones in the current directory.'
                .format(__app_name__, __version__),
                epilog='EPILOG')
    # e.g. '*.mp3' or '*'
    parser.add_argument('include', metavar='INCLUDE_PATTERN', type=str,
                        help='Specify the files to include with a wildcard-mask. It can be a list'\
                        'seperated by {}.'.format(os.pathsep))
    # --recursive, -r, -R
    parser.add_argument('-r', '--recursive', action='store_true', dest='argRecursiv',
                       help='Do the job recursivly through the sub-directories.')
    # --action
    # --no-rm-security-question
    # --no-mv-security-question
    # --input-dir, -i
    parser.add_argument('-i', '--input-dir', metavar='DIR', dest='inputDir',
                        default=os.path.abspath(os.curdir), type=str,
                        help='The directory where to start from (default: current working directory).')
    # --output-dir, --output-cwd
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o', '--output-dir', metavar='DIR', dest='outputDir', type=str,
                       help='Use the specified directory for output.')
    group.add_argument('-cwd', '--output-cwd', dest='outputCwd', action='store_true',
                       help='Use the current working directory as output directory.')

    # store all arguments in objects/variables of the local namespace
    locals().update(vars(parser.parse_args()))

    # prepare
    include = include.split(os.pathsep)
    rootDir = os.path.expanduser(os.path.normpath(inputDir))
    orgFiles = []
    inputDirs = [rootDir]
    if outputCwd:
        # current working directory for output
        outputDir = os.path.abspath(os.curdir)
    else:
        if outputDir:
            # user (per argument) specified directory for output
            outputDir = os.path.expanduser(os.path.normpath(outputDir))

    # recursive
    if argRecursiv == True:
        for root, dirs, names in os.walk(rootDir):
            if '{}.'.format(os.sep) not in root:
                inputDirs += [root]

    # create a list of each related file
    orgFiles += _GetFiles(inputDirs, include)

    # random ordered unique numbers
    randNumbers = list(range(1, len(orgFiles)))
    random.shuffle(randNumbers)

    newFiles = []
    formatStr = '{:0' + str(1+len(str(len(orgFiles)))) + '}'

    for org, rnd in zip(orgFiles, randNumbers):
        org_name, org_ext = os.path.splitext(org)
        org_name = org_name.rsplit(os.sep, 1)[0]
        # TODO: more pythonic way to do that?
        if outputDir:
            newFiles += [ outputDir + os.sep + formatStr.format(rnd) + org_ext ]
        else:
            newFiles += [ org_name + os.sep + formatStr.format(rnd) + org_ext ]

    for org, new in zip(orgFiles, newFiles):
        print('{};{}'.format(org, new))

    sys.exit()

