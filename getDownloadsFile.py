import os

from glob import glob


def get_downloads_file(filename_prefix):
    pattern = fr'C:\Users\*\Downloads\{filename_prefix}*'
    files = glob(pattern)
    if not files:
        input(f'No file found for pattern {pattern}'
              '[Press Enter to Exit]')
        exit(1)

    files.sort(key=os.path.getmtime, reverse=True)

    print(f'Using {files[0]}: modified {os.path.getmtime(files[0])}')
    return files[0]
