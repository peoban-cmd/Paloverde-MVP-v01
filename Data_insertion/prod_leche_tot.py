import re, sys
from pathlib import Path
from datetime import datetime

# Import own code
software_path = re.sub('Python.*', 'Python',str(Path(__file__).resolve().parent))
shared_functions_path = f'{software_path}/Shared_functions'
append_paths = [shared_functions_path]
for i in append_paths:
    sys.path.append(i)
from data_insertion_abstract_class import AbstractPythonClass

class ProdLecheTot(AbstractPythonClass):
    def data_parser(self,row):
        keys = ['leche_litros','queso_litros','fecha','numero_vacas']
        # Compare two lists
        equal = [0  if key == column else 1 for key,column in zip(keys,self.df.columns)]
        if 1 in equal:
            print('ERROR: data_parser. Not all the key have been declared')
            print(self.df.columns)
            return
        inputs = {}
        values = self.df.to_numpy().astype(object)
        inputs['leche_litros'] = float(values[row,0])
        inputs['queso_litros'] = float(values[row, 1])
        inputs['fecha'] = datetime.strptime((values[row,2]), '%Y-%m-%d').date()
        inputs['numero_vacas'] = int(values[row,3])

        self.inputs = inputs
        return