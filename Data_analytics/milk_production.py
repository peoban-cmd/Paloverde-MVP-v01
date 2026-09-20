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
    def create_table(self,y_var):
        one_week = {'label':'Una semana','week_delta':1}
        two_weeks = {'label': 'Dos semanas', 'week_delta': 2}
        all = {'label': 'Totalidad datos', 'week_delta': 1e3}
        categories = [one_week,two_weeks,all]
        columns = ['Categoría','Promedio','Max','Min']
        data = np.zeros((len(categories),len(columns)),dtype=object)
        for counter, category in enumerate(categories):
            lim_date = pd.to_datetime(date.today()-timedelta(weeks=category['week_delta']))
            df_subset = self.df[self.df['fecha']>=lim_date]
            data[counter,0] = category.get('label')
            data[counter,1] = df_subset[y_var].mean()
            data[counter,2] = df_subset[y_var].max()
            data[counter,3] = df_subset[y_var].min()
        output = pd.DataFrame(data,columns=columns)
        output.to_csv(f'{self.results_path}/{y_var}.csv',index=False)
        print(output)
    def plot_milk_production(self):
        date = self.df_date
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
        df_date = self.df_date
        plt.plot(df_date,self.df[y_var])
        plt.xlabel('Fecha')
        plt.ylabel(y_label)
        plt.xticks(rotation=90)
        # Adjust y max
        if y_var == 'numero_vacas':
            y_max = 20
            plt.yticks(np.arange(0,y_max + 1,4))
            plt.yticks(np.arange(0, 21, 1), minor=True)
        else:
            y_max = 1.1*self.df[y_var].max()
        plt.ylim(0,y_max)
        # Add vertical lines for the weeks
        for i in range(1,self.week_span):
            lim_date = date.today()-timedelta(weeks=i)
            lim_date = lim_date.strftime('%d-%b')
            plt.vlines(x=lim_date,ymin=0,ymax=y_max,linestyle='dashed',color='red')
        plt.tight_layout()
        plt.savefig(f'{self.results_path}/{fig_name}.png',dpi=250)
        plt.close()
        return
    def query(self):
        self.week_span = 3
        limit_date = date.today() - timedelta(weeks=self.week_span)
        query = f"SELECT * from prod_leche_tot WHERE fecha > '{limit_date}'"
        self.df = pd.read_sql(query, self.engine)
        return
    def export_data(self):
        self.df['fecha'] = pd.to_datetime(self.df['fecha'])
        self.df_date = self.df['fecha'].dt.strftime('%d-%b')
        self.df['leche_por_vaca'] = self.df['leche_litros'] / self.df['numero_vacas']
        # Plots
        # self.plot_milk_production()
        self.create_table('leche_litros')
        self.create_table('leche_por_vaca')
        self.plot_function('leche_litros','Producción total de leche (L)','ProduccionTotalLeche')
        self.plot_function('queso_litros', 'Leche para queso (L)', 'LecheQueso')
        self.plot_function('numero_vacas', 'Número de vacas ordeñadas', 'VacasOrdenadas')
        self.plot_function('leche_por_vaca','Promedio de leche por vaca (L)','PromedioLechePorVaca')
        print(f'Data exported for "{self.case_config.function_name}"')
        return