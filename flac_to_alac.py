#!/usr/bin/env python3

"""FLAC to ALAC Audio File Format Converter

This script is useful for making a copy of a music or
audio library containing FLAC files in which all FLAC
files are converted to Apple Lossless (ALAC) format.
The typical use case would be so that the library can
be imported into Apple Music or iTunes, which do not
support the FLAC format.

This script is non-destructive and creates a complete
copy of your libary, preserving the directory structure
and including all non-FLAC files such as artwork, log
files, .mp3 or .aac files, etc. FLAC files will copied
to ALAC files, all other files will simply be copied.

Suggested usage:
./flac_to_alac.py --input <path/to/existing/library> --output <path/to/directory/for/new/library>
"""

import argparse
import os
import subprocess
import sys


def get_args() -> dict:
    """Parse input arguments. User will be prompted for any required info not specified on command line."""
    parser = argparse.ArgumentParser(description="FLAC to ALAC audio file format converter")
    parser.add_argument('-i', '--input', metavar='', help='Path to input directory with files to be converted')
    parser.add_argument('-o', '--output', metavar='', help='Path to output directory to which files will be sent')
    parser.add_argument('-w', '--overwrite', metavar='', help='Overwrite output files if they already exist? [y/N]')
    args = parser.parse_args()

    if args.input is None:
        args.input = input("Enter full path to music library:\n")
    if args.output is None:
        args.output = input("Enter full path to desired output directory:\n")
    if args.overwrite is None:
        args.overwrite = input("Overwrite output files if they already exist? [y/N]\n")
    if args.overwrite.lower() == 'y':
        args.overwrite = '-y'
    else:
        args.overwrite = '-n'
    
    return args


def validate_directory(path: str) -> None:
    """Make sure directory specified by user is real"""
    try:
        _ = os.listdir(path)
    except FileNotFoundError:
        sys.exit(f"Invalid directory path: nothing found at {path}")
    except NotADirectoryError:
        sys.exit(f"Invalid directory path: {path} is not a directory")


def process_files(target: str, destination: str, overwrite_flag: str) -> None:
    """Copy files and directories, converting FLAC to ALAC in the process"""
    for filename in os.listdir(target):
        path = os.path.join(target, filename)
        if os.path.isdir(path):
            output_dir = destination + '/' + filename
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            process_files(path, output_dir, overwrite_flag)
            continue
        extension = path.split('.')[-1]
        if extension.lower() == 'flac':
            modified_filename = ''.join(filename.split(extension)[:-1]) + 'm4a'
            outfile = os.path.join(destination, modified_filename)
            subprocess.call(['ffmpeg', overwrite_flag, '-v', 'warning', '-i', path, '-c:a', 'alac', '-c:v', 'copy', outfile])
        else:
            outfile = os.path.join(destination, filename)
            subprocess.call(['rsync', '-u', path, outfile])


def main() -> None:
    args = get_args()
    for path in (args.input, args.output):
        validate_directory(path)
    process_files(args.input, args.output, args.overwrite)


if __name__ == '__main__':
    main()
