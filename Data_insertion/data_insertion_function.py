import sys, re
from pathlib import Path

debug = False
if debug:
    project_path = "/home/pedro/Documents/PaloVerde/Project"
    table_name = 'prod_leche_tot'
else:
    project_path = sys.argv[1]
    table_name = sys.argv[2]

# Implemented functions
from prod_leche_tot import ProdLecheTot
implementations = {"prod_leche_tot": ProdLecheTot}

software_path = re.sub('MVP-v01.*', 'MVP-v01',str(Path(__file__).resolve().parent))
shared_functions_path = f'{software_path}/Shared_functions'
append_paths = [shared_functions_path, project_path + '/Configuration']
for i in append_paths:
    sys.path.append(i)
from data_insertion_abstract_class import AbstractPythonClass
from configuration_class import CaseConfig # Dataclass fro case configuration
from case_config import db # Import the case configuration

case_config = CaseConfig(project_path = project_path, function_name=table_name,
                         user = db.get("user"),password = db.get("password"),localhost = db.get("localhost") ,port = db.get("port") ,database = db.get("database"),
                         )

object = implementations[case_config.function_name](case_config, table_name)
object.insert()
object.close()