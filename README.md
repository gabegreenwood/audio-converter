# audio-converter

**FLAC to ALAC Audio File Format Converter**

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

`./flac_to_alac.py --input <path/to/existing/library> --output <path/to/directory/for/new/library>`
