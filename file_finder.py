import time
from glob import glob
from os.path import getmtime


class FileFinder:
    def __init__(self, filename_prefix, folders=None):
        self.files = []

        if not folders:
            folders = [
                '.\\',
                'C:\\Users\\*\\Downloads\\',
            ]

        for i, folder in enumerate(folders):
            if folder[-1] != '\\':  # if there's no trailing slash, add it
                folder += '\\'

            for g in glob(fr'{folder}{filename_prefix}*'):
                self.files.append(FF_File(g, i))  # g, i = glob filename, index of folder

        self.files.sort(reverse=True)

    def get_file(self):
        return self.files[0].full_path

    def get_csv_file_info(self, min_header):
        """gets the most recent csv file with these headers, returns (path, delimiter)"""
        self.check_csv_files(min_header)
        return self.files[0].full_path, self.files[0].delimiter

    def check_csv_files(self, min_header):
        """removes csv's from file list if they don't have at least the columns specified"""
        for f in self.files[::-1]:
            f.calc_csv_info()
            if not f.header_set > set(min_header):
                self.files.remove(f)

        if len(self.files) == 0:
            print(f'There are no files that meet the minimum headers of\n[{min_header}]')


class FF_File:
    def __init__(self, full_path, folder_index=-1):
        self.full_path = full_path
        self.folder_index = folder_index

        self.time_modified = time.strftime('%Y/%m/%d %a %H:%M:%S', time.gmtime(getmtime(full_path)))

        # CSV specific fields
        self.header_set = set()
        self.num_records = 0
        self.delimiter = ''

    def __lt__(self, other):  # enables sorting using native methods
        if self.folder_index > other.folder_index:
            return True
        elif self.folder_index == other.folder_index and self.time_modified < other.time_modified:
            return True
        else:
            return False

    def calc_csv_info(self):
        with open(self.full_path, 'r') as f:
            try:
                header = f.readline()
                self.num_records = f.read().count('\n') + 1
            except UnicodeDecodeError:
                print(f'{self.full_path} isn\'t a unicode file. Skipping...')
                return

        header = header.strip()

        # figure out which delimiter is being used (and also calc header_set)
        for sep in [',', '\t', ';']:
            h = set(header.split(sep))
            if len(h) > len(self.header_set):
                self.delimiter = sep
                self.header_set = h

        # remove quotes from header
        for h in self.header_set:
            if h != '' and h[0] + h[-1] == '""':
                self.header_set.remove(h)
                self.header_set.add(h[1:-1])


if __name__ == '__main__':
    ff = FileFinder('student.export')
    a = ff.get_csv_info(['First_Name'])
    raise hell  # force into debugger
