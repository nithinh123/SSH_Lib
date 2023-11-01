class CSVParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def parse_file(self):
        for row in open(self.file_path, "r"):
            yield row

    @staticmethod
    def info():
        return "CSV Parser class"
