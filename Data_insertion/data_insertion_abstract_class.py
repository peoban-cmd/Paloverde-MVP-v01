from abc import ABC, abstractmethod
import psycopg2
import pandas as pd

class AbstractPythonClass(ABC):
    def __init__(self,case_config,table_name):
        self.case_config = case_config
        self.table_name = table_name
        self.conn = psycopg2.connect(
            host=case_config.localhost,
            port=case_config.port,
            database=case_config.database,
            user=case_config.user,
            password=case_config.password
        )
        self.cur = self.conn.cursor()
        self.df = pd.read_csv(f'{self.case_config.project_path}/Data_insertion/{self.table_name}.csv')
    @abstractmethod
    def data_parser(self):
        """"
        Parse the data to a dictionary, the function is specified for each table to be inserted
        """
        pass
    def insert(self):
        for row in range(self.df.shape[0]):
            self.data_parser(row)
            inputs = self.inputs
            keys = inputs.keys()
            # Insert
            str1 = f'INSERT INTO {self.table_name} ('
            for count, key in enumerate(keys):
                str1 += key
                if count != len(keys) - 1:
                    str1 += ','
            str2 = ') VALUES (%s, %s, %s);'
            query = str1 + str2

            self.cur.execute(
                query,
                tuple(inputs.values())
            )

            # Commit the transaction
            self.conn.commit()
            print(f"Data inserted successfully for {inputs.get('fecha')}.")
        return
    def close(self):
        self.cur.close()
        self.conn.close()