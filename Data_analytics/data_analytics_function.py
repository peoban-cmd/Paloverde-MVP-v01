"""
Interface function for data analytics

To add a new functionality or implementation:
- import the file and the module
- Add the name to the 'implementations' dictionary
"""

import sys, re, os
from pathlib import Path

# Inputs
project_path = "/home/pedro/Documents/PaloVerde/Project"
function_name='milk_production'

# Implemented functions
from milk_production import MilkProduction
implementations = {"milk_production": MilkProduction}


software_path = re.sub('Python.*', 'Python',str(Path(__file__).resolve().parent))
shared_functions_path = f'{software_path}/Shared_functions'
append_paths = [shared_functions_path, project_path + '/Configuration']
for i in append_paths:
    sys.path.append(i)
from configuration_class import CaseConfig # Dataclass fro case configuration
from case_config import db # Import the case configuration

case_config = CaseConfig(project_path = project_path, function_name=function_name,
                         user = db.get("user"),password = db.get("password"),localhost = db.get("localhost") ,port = db.get("port") ,database = db.get("database"),
                         )

object = implementations[case_config.function_name](case_config)
object.query()
object.export_data()