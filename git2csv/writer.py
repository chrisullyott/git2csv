import os
import csv

class CsvWriter:
    def __init__(self, name, data, directory=None):
        self.name = name
        self.data = data
        self.directory = directory if directory else 'output'

    def get_filepath(self):
        filename = '{}.csv'.format(self.name)
        return os.path.join(self.directory, filename)

    def write(self):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        with open(self.get_filepath(), 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
