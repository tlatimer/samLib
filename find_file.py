from datetime import datetime
from os.path import getmtime
from glob import glob


def find_file(filename_prefix):
    """Checks each dir, then if it finds file(s) in that dir returns the most recent one"""
    patterns = [
        fr'.\{filename_prefix}*',
        fr'..\master csvs\{filename_prefix}*',
        fr'C:\Users\*\Downloads\{filename_prefix}*',
    ]

    for p in patterns:
        files = glob(p)
        if files:
            break

    assert files  # fails if no files were found

    files.sort(key=getmtime, reverse=True)

    modified_time = datetime.fromtimestamp(getmtime(files[0])).strftime('%Y/%m/%d %a %H:%M:%S')

    print(f'Using {files[0]}: modified {modified_time}')
    return files[0]
