import pandas as pd

class DB:
    def __init__(self, path_data):
        self._df_car = pd.read_csv(path_data, sep='\t')

    def getMatricula(self, matricula):
        return self._df_car.query(f"Matricula == '{matricula}'")['Pos_date'].values[0]