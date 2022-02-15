#!/usr/local/bin/python3

import argparse
import glob
import logging
import os
import pathlib
import sys
import tarfile
import zipfile

import rarfile

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger(__name__)

DEFAULT_OUTPUT_FILE = './output.txt'

RAR_EXTENSIONS = ['.rar']
ZIP_EXTENSIONS = ['.zip']
GZ_EXTENSIONS = ['.gz']
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


def scan_gz(filepath):
    """ Scan a .tar.gz file. """
    return tarfile.open(filepath, 'r:gz').getnames()


def write_to_file(output, file, docs):
    """ Write to the output file."""
    with open(output, 'a') as f:
        for doc in docs:
            out = '{}\t{}'.format(file, doc)
            log.info(out)
            f.write('{}\n'.format(out))


def main():
    parser = argparse.ArgumentParser(description='Find docs recursively in a directory including in archives')
    parser.add_argument('--path', type=str, help='The path to start the search from')
    parser.add_argument('--output', type=str, help='The output file', default=DEFAULT_OUTPUT_FILE)
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

    # .tar.gz files.
    gz_files = filter_by_extensions(files, GZ_EXTENSIONS)
    filter_gz_files = [x for x in gz_files if x.find('.tar') != -1]
    for gz_file in filter_gz_files:
        docs = filter_by_extensions(scan_gz(gz_file), DOC_EXTENSIONS)
        write_to_file(args.output, gz_file, docs)

    return 0


if __name__ == "__main__":
    sys.exit(main())
