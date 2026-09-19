import math, re, ast, sys, os, subprocess
import numpy as np
from pathlib import Path
import pandas as pd
from datetime import date, timedelta
from matplotlib import pyplot as plt

# Import own code
software_path = re.sub('Python.*', 'Python',str(Path(__file__).resolve().parent))
shared_functions_path = f'{software_path}/Shared_functions'
append_paths = [shared_functions_path]
for i in append_paths:
    sys.path.append(i)
from data_analytics_abstract_class import AbstractPythonClass

class MilkProduction(AbstractPythonClass):
    def plot_milk_production(self):
        date = self.date
        plt.plot(date,self.df['leche_litros'],label='Total')
        plt.plot(date, self.df['queso_litros'], label='Queso')
        # self.plot_function('leche_litros','Total de leche (L)','ProduccionTotalLeche')
        plt.xlabel('Fecha')
        plt.ylabel('Producción de leche (L)')
        plt.xticks(rotation=90)
        plt.ylim(0,1.1*self.df['leche_litros'].max())
        plt.tight_layout()
        plt.legend(loc='upper right')
        plt.savefig(f'{self.results_path}/ProduccionLeche.png',dpi=250)
        plt.close()

        return
    def plot_function(self,y_var,y_label,fig_name):
        date = self.date
        plt.plot(date,self.df[y_var])
        plt.xlabel('Fecha')
        plt.ylabel(y_label)
        plt.xticks(rotation=90)
        plt.ylim(0,1.1*self.df[y_var].max())
        if y_var == 'numero_vacas':
            plt.yticks(np.arange(0,24,4))
            plt.yticks(np.arange(0, 21, 1), minor=True)
        plt.tight_layout()
        plt.savefig(f'{self.results_path}/{fig_name}.png',dpi=250)
        plt.close()
        return
    def query(self):
        limit_date = date.today() - timedelta(weeks=3)
        query = f"SELECT * from prod_leche_tot WHERE fecha > '{limit_date}'"
        self.df = pd.read_sql(query, self.engine)
        return
    def export_data(self):
        self.df['leche_por_vaca'] = self.df['leche_litros'] / self.df['numero_vacas']
        date = pd.to_datetime(self.df['fecha'])
        self.date = date.dt.strftime('%d-%b')
        # Plots
        # self.plot_milk_production()
        self.plot_function('leche_litros','Producción total de leche (L)','ProduccionTotalLeche')
        self.plot_function('queso_litros', 'Leche para queso (L)', 'LecheQueso')
        self.plot_function('numero_vacas', 'Número de vacas ordeñadas', 'VacasOrdenadas')
        self.plot_function('leche_por_vaca','Promedio de leche por vaca (L)','PromedioLechePorVaca')
        print(f'Data exported for "{self.case_config.function_name}"')
        return