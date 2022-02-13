#!/usr/local/bin/python3

import glob
import logging
import os
import pathlib
import sys
import zipfile

import rarfile
import argparse

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger(__name__)

DEFAUT_OUTPUT_FILE = './output.txt'
RAR_EXTENSIONS = ['.rar']
ZIP_EXTENSIONS = ['.zip']
# .gz
# .tar.gz
DOC_EXTENSIONS = ['.txt', '.doc', '.docx', '.odt', '.rtf']


def get_files(root_dir):
    """ Get all files in the root directory. """
    return list(glob.iglob(root_dir + '**/**', recursive=True))


def filter_by_extensions(files, extensions):
    """ Filter the file names by a list of extensions."""
    return [file for file in files if pathlib.Path(file).suffix in extensions]


def scan_rar(filepath):
    """ Scan the files inside of a .rar archive. """
    return [f.filename for f in rarfile.RarFile(filepath).infolist()]


def scan_zip(filepath):
    """ Scan the files inside of a .zip archive. """
    return zipfile.ZipFile(filepath).namelist()


def write_to_file(output, file, docs):
    """ Write to the output file."""
    with open(output, 'a') as f:
        for doc in docs:
            out = '{}\t{}'.format(file, doc)
            log.info(out)
            f.write('{}\n'.format(out))


def main():
    parser = argparse.ArgumentParser(description='Find docs recursively in a directory including in archives.')
    parser.add_argument('--path', type=str, help='The path the start the search from')
    parser.add_argument('--output', type=str, help='The output file', default=DEFAUT_OUTPUT_FILE)
    parser.add_argument('--skip-txt', action='store_true', help='Skip .txt files')

    args = parser.parse_args()

    if args.path is None:
        log.error('The `path` argument is required')
        return 1

    open(args.output, 'w')

    files = get_files(args.path)

    if args.skip_txt:
        DOC_EXTENSIONS.remove('.txt')

    # root files.
    docs = filter_by_extensions(files, DOC_EXTENSIONS)
    write_to_file(args.output, 'root', docs)

    # .rar files.
    rar_files = filter_by_extensions(files, RAR_EXTENSIONS)
    for rar_file in rar_files:
        docs = filter_by_extensions(scan_rar(rar_file), DOC_EXTENSIONS)
        write_to_file(args.output, rar_file, docs)

    # .zip files.
    zip_files = filter_by_extensions(files, ZIP_EXTENSIONS)
    for zip_file in zip_files:
        docs = filter_by_extensions(scan_zip(zip_file), DOC_EXTENSIONS)
        write_to_file(args.output, zip_file, docs)

    return 0


if __name__ == "__main__":
    sys.exit(main())
