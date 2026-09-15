import pandas as pd

def read_wells(path): return pd.read_csv(path)
def read_layers(path): return pd.read_excel(path)
def read_pumping_test(path): return pd.read_csv(path, sep="\t")

def print_table_info(name, table):
    print(f"\n--- {name} ---")
    print("Форма:", table.shape)
    print("Столбцы:", table.columns.tolist())
    print("Типы:\n", table.dtypes)
    print("Первые строки:\n", table.head())

class DatasetInfo:
    def __init__(self, name, table):
        self.name = name
        self.rows, self.columns = table.shape

    def describe(self):
        return f"{self.name}: {self.rows} строк, {self.columns} столбцов"