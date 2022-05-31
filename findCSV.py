import time
from glob import glob
from os import path

DELIMITER = ','


def find_csv(minimum_headers, folder='C:\\Users\\*\\Downloads', f_name='*.csv'):
    minimum_headers_set = set(minimum_headers)

    if len(minimum_headers) > len(minimum_headers_set):
        raise Exception('minimum_headers are not unique')

    if folder[-1] != '\\':  # if there's no trailing slash, add it
        folder += '\\'

    pattern = f'{folder}{f_name}'
    files = glob(pattern)
    if not files:
        raise Exception(f"no csv in {pattern}")

    files.sort(key=path.getmtime, reverse=True)

    for file in files:
        with open(file, 'r') as f:
            header = f.readline()
            header = header.strip()
            header = header.split(DELIMITER)

            header_set = set(header)
            # if len(header) > len(header_set):
            #     print(f'{file}\t has duplicate fields in the header. Skipping...')

            if header_set >= minimum_headers_set:
                file_modified = time.strftime('%Y/%m/%d %a %H:%M:%S', time.gmtime(path.getmtime(file)))
                print(f'Using {file}    modified {file_modified}')
                return file

    raise Exception(f"no csv found with valid header in {pattern}")


find_csv(['Transaction Date'])
