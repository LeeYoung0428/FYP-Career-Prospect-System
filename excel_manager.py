import pandas as pd


class ExcelManager:
    def __init__(self, filename):
        print("Reading excel file")
        self.df = pd.read_excel(filename)

    def get(self):
        return self.df.to_dict("records")