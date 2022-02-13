#!/usr/local/bin/python3

import glob
import logging
import os
import pathlib
import sys
import zipfile

import rarfile

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

log = logging.getLogger(__name__)

OUTPUT_FILE = './output.txt'
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


def write_to_file(file, docs):
    """ Write to the output file."""
    with open(OUTPUT_FILE, 'a') as f:
        for doc in docs:
            out = '{}\t{}'.format(file, doc)
            log.info(out)
            f.write('{}\n'.format(out))


def main(argv):
    print(argv[0])
    if len(argv) == 0:
        log.error('The path argument is required')
        return 1

    open(OUTPUT_FILE, 'w')

    files = get_files(argv[0])

    # root files.
    docs = filter_by_extensions(files, DOC_EXTENSIONS)
    write_to_file('root', docs)

    # .rar files.
    rar_files = filter_by_extensions(files, RAR_EXTENSIONS)
    for rar_file in rar_files:
        docs = filter_by_extensions(scan_rar(rar_file), DOC_EXTENSIONS)
        write_to_file(rar_file, docs)

    # .zip files.
    zip_files = filter_by_extensions(files, ZIP_EXTENSIONS)
    for zip_file in zip_files:
        docs = filter_by_extensions(scan_zip(zip_file), DOC_EXTENSIONS)
        write_to_file(zip_file, docs)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
