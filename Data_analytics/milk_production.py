import math, re, ast, sys, os, subprocess
import numpy as np
from pathlib import Path
import pandas as pd
from datetime import date, timedelta

# Import own code
software_path = re.sub('Python.*', 'Python',str(Path(__file__).resolve().parent))
shared_functions_path = f'{software_path}/Shared_functions'
append_paths = [shared_functions_path]
for i in append_paths:
    sys.path.append(i)
from data_analytics_abstract_class import AbstractPythonClass

class MilkProduction(AbstractPythonClass):
    def query(self):
        limit_date = date.today() - timedelta(weeks=1)
        query = f"SELECT * from prod_leche_tot WHERE fecha > '{limit_date}'"
        self.df = pd.read_sql(query, self.engine)
        return
    def export_data(self):
        print(self.df)
        print(f'Export data in {os.path.basename(__file__)}')
        # df = pd.DataFrame(self.arr, columns=self.obj.element_keys)
        # df.to_csv(f'{self.output_name}.csv', index=False)
        # np.save(f'{self.output_name}', self.arr)
        return